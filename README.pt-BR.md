# 🚗 PlateVision

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-orange)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![Status](https://img.shields.io/badge/Status-Ativo-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

🇺🇸 [English version](README.md)

---

Sistema de **detecção de placas veiculares em tempo real** utilizando **YOLOv8** e **OpenCV**.

---

## 📸 Exemplos

### Detecção em cenários reais

![Exemplo 1](frames_salvos/deteccao_20260504_115923.png)
![Exemplo 2](frames_salvos/deteccao_20260428_183140.png)
![Exemplo 3](frames_salvos/deteccao_20260504_115840.png)
![Example 4](frames_salvos/deteccao_20260504_115857.jpg)

---

## ✨ Funcionalidades

* 🔍 Detecção de placas em **imagens estáticas**
* 🎮 Captura de tela em **tempo real (jogos/streams)**
* 💾 Salvamento automático de:

  * recortes das placas (crops)
  * frames anotados
* ⚡ Execução otimizada (CPU/GPU)
* 🧠 Controle de memória para evitar travamentos

---

## 🛠️ Tecnologias utilizadas

* Python
* YOLOv8 (Ultralytics)
* OpenCV
* NumPy
* MSS (captura de tela)

---

## 📦 Instalação

```bash
git clone https://github.com/seuusuario/PlateVision.git
cd PlateVision
pip install -r requirements.txt
```

---

## 🧠 Modelo YOLO

Este projeto utiliza um modelo treinado de detecção de placas.

📥 Você pode obter um modelo em:

* Roboflow Universe (busque por *license plate detection*)

Depois, salve em:

```bash
modelos/detector_placas.pt
```

---

## 🚀 Como usar

### 📷 Imagem estática

```bash
python platevision.py --imagem imagens_teste/placa1.png
```

---

### 🎮 Captura de tela (tempo real)

```bash
python platevision.py --jogo --cpu
```

> ⚠️ Recomendado usar `--cpu` para maior estabilidade

---

## ⌨️ Controles

|ㅤTeclaㅤ| Açãoㅤㅤㅤㅤ|  
|ㅤ------- | ----------------|  
ㅤQㅤㅤ~ㅤSair ㅤㅤㅤ  
ㅤSㅤㅤ ~ㅤSalvar frame

---

## 📁 Pastas geradas

* `crops/` → recortes das placas detectadas
* `frames_salvos/` → frames anotados salvos

---

## 🧪 Testado em

* ✔️ Imagens e vídeos reais de veículos
* ✔️ Captura de tela (ex: GTA V, YouTube)
* ✔️ Windows 10/11
* ✔️ Python 3.8+

---

## ⚠️ Observações

* As imagens podem conter **placas parcialmente anonimizadas**
* O arquivo `.pt` **não está incluído** no repositório

---

## 🔮 Próximos passos

* [ ] OCR para leitura da placa
* [ ] Interface gráfica (GUI)
* [ ] Suporte a webcam
* [ ] API (Flask ou FastAPI)

---

## 🤝 Contribuição

Sinta-se à vontade para abrir issues ou pull requests.

---

## 📄 Licença

Licença MIT

---

## 👨‍💻 Autor

Desenvolvido por **Maurício Santos**

---
