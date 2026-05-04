"""
PlateVision - Detecção de placas veiculares com YOLOv8
Modos: imagem estática ou captura de tela (jogos/stream)
"""

import cv2
import numpy as np
import argparse
import os
import time
import gc
from pathlib import Path

# ========== CONFIGURAÇÕES ==========
MODELO_PATH = "modelos/detector_placas.pt"
CONFIANCA_YOLO = 0.45
IOU_THRESHOLD = 0.45
MARGEM_CROP = 8
MONITOR_INDEX = 1
# ===================================

class DetectorYOLO:
    """Carrega modelo YOLO e retorna bounding boxes de placas."""
    def __init__(self, modelo_path: str, forcar_cpu: bool = False):
        from ultralytics import YOLO
        if not os.path.exists(modelo_path):
            raise FileNotFoundError(f"\n[ERRO] Modelo não encontrado: {modelo_path}")
        print(f"Carregando modelo: {modelo_path}")
        t = time.time()
        self.model = YOLO(modelo_path)
        if forcar_cpu:
            self.model.to('cpu')
            print("YOLO rodando em CPU")
        print(f"Modelo carregado em {time.time()-t:.1f}s")

    def detectar(self, frame: np.ndarray) -> list[dict]:
        resultados = self.model(frame, conf=CONFIANCA_YOLO, iou=IOU_THRESHOLD, verbose=False)
        deteccoes = []
        h, w = frame.shape[:2]
        for result in resultados:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                conf = float(box.conf[0])
                x1m = max(0, x1 - MARGEM_CROP)
                y1m = max(0, y1 - MARGEM_CROP)
                x2m = min(w, x2 + MARGEM_CROP)
                y2m = min(h, y2 + MARGEM_CROP)
                crop = frame[y1m:y2m, x1m:x2m]
                deteccoes.append({
                    "bbox": (x1, y1, x2, y2),
                    "confianca": conf,
                    "crop": crop
                })
        return deteccoes

def desenhar_deteccoes(frame, deteccoes):
    vis = frame.copy()
    for det in deteccoes:
        x1, y1, x2, y2 = det["bbox"]
        conf = det["confianca"]
        cor = (0, int(100 + 155*conf), 0)
        cv2.rectangle(vis, (x1, y1), (x2, y2), cor, 2)
        label = f"Placa {conf:.2f}"
        (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        cv2.rectangle(vis, (x1, y1 - lh - 8), (x1 + lw + 4, y1), cor, -1)
        cv2.putText(vis, label, (x1 + 2, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 1)
    return vis

def adicionar_hud(frame, fps, n_deteccoes):
    cv2.rectangle(frame, (0,0), (280,45), (0,0,0), -1)
    cv2.putText(frame, f"FPS: {fps:.1f}  Placas: {n_deteccoes}", (8,18),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0,255,0), 1)
    cv2.putText(frame, "[Q] Sair  [S] Salvar frame", (8,38),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180,180,180), 1)
    return frame

def modo_imagem(detector, caminho):
    img = cv2.imread(caminho)
    if img is None:
        print(f"Erro ao carregar: {caminho}")
        return
    deteccoes = detector.detectar(img)
    print(f"Detecções: {len(deteccoes)}")
    for i, d in enumerate(deteccoes):
        x1,y1,x2,y2 = d["bbox"]
        print(f"  [{i+1}] ({x1},{y1},{x2},{y2}) conf={d['confianca']:.2f}")
        os.makedirs("crops", exist_ok=True)
        cv2.imwrite(f"crops/crop_{i+1}_{Path(caminho).stem}.jpg", d["crop"])
    vis = desenhar_deteccoes(img, deteccoes)
    cv2.imshow("PlateVision", vis)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    del img, deteccoes
    gc.collect()

def modo_jogo(detector):
    try:
        import mss
    except ImportError:
        print("Instale: pip install mss")
        return
    print("Captura de tela ativa. Pressione Q para sair.")
    fps = 0.0
    frames = 0
    t_fps = time.time()
    with mss.mss() as sct:
        monitor = sct.monitors[MONITOR_INDEX]
        while True:
            shot = sct.grab(monitor)
            frame = cv2.cvtColor(np.array(shot), cv2.COLOR_BGRA2BGR)
            deteccoes = detector.detectar(frame)
            vis = desenhar_deteccoes(frame, deteccoes)
            vis = adicionar_hud(vis, fps, len(deteccoes))
            h,w = vis.shape[:2]
            cv2.imshow("PlateVision", cv2.resize(vis, (w//2, h//2)))
            frames += 1
            if time.time() - t_fps >= 1.0:
                fps = frames / (time.time() - t_fps)
                frames, t_fps = 0, time.time()
            if frames % 30 == 0:
                gc.collect()
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                ts = time.strftime("%Y%m%d_%H%M%S")
                os.makedirs("frames_salvos", exist_ok=True)
                cv2.imwrite(f"frames_salvos/deteccao_{ts}.jpg", vis)
                print(f"Frame salvo: frames_salvos/deteccao_{ts}.jpg")
    cv2.destroyAllWindows()
    gc.collect()

def main():
    parser = argparse.ArgumentParser(description="PlateVision - Detecção de placas")
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--imagem", type=str, help="Caminho da imagem estática")
    grupo.add_argument("--jogo", action="store_true", help="Captura de tela (jogos/stream)")
    parser.add_argument("--cpu", action="store_true", help="Forçar uso da CPU (recomendado para estabilidade)")
    args = parser.parse_args()

    os.makedirs("modelos", exist_ok=True)
    try:
        detector = DetectorYOLO(MODELO_PATH, forcar_cpu=args.cpu)
    except FileNotFoundError as e:
        print(e)
        print("Baixe um modelo de detecção de placas (ex: do Roboflow) e salve em 'modelos/detector_placas.pt'")
        return

    if args.imagem:
        modo_imagem(detector, args.imagem)
    elif args.jogo:
        modo_jogo(detector)

if __name__ == "__main__":
    main()