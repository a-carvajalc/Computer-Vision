# CV1 Assignment 1: Computer Vision Fundamentals

Este proyecto implementa una estructura de aprendizaje tipo TDD (Test-Driven Development) para el laboratorio 1 de Computer Vision, basado en el material del profesor en `Lab_1.pdf`.

## 📋 Contenidos

El Assignment 1 cubre tres temas fundamentales:

1. **Thin Lens Equation** - Ecuaciones ópticas y formación de imágenes
2. **Geometric Transformations** - Transformaciones 2D y 3D (traslación, rotación, transformaciones afines, proyectivas)
3. **OpenCV Fundamentals** - Operaciones básicas de imágenes (filtros, blending, brillo/contraste, ecualización de histograma, transformaciones geométricas)

## 🗂️ Estructura del Proyecto

```
Assignment1/
├── LEARNING_GUIDE.md           # Guía completa con teoría y ejemplos
├── README.md                    # Este archivo
├── requirements.txt             # Dependencias Python
├── tests/                       # Suite de pruebas completa (NO MODIFICAR)
│   ├── test_thin_lens.py       # ~280 líneas, 28 tests
│   ├── test_transformations.py # ~380 líneas, 38 tests
│   └── test_opencv_basics.py   # ~370 líneas, 35 tests
└── src/                         # Tu código aquí (PARA IMPLEMENTAR)
    ├── __init__.py
    ├── thin_lens.py            # 7 funciones para implementar
    ├── transformations.py       # 12 funciones para implementar
    └── opencv_operations.py     # 12+ funciones para implementar
```

## ⚡ Inicio Rápido

### 1. Instalar dependencias

```bash
cd /home/work/Develop/Master/CV1/Assignment1
pip install -r requirements.txt
```

### 2. Verificar que los tests se ejecutan

```bash
# Opción 1: Con pytest
pytest tests/ -v

# Opción 2: Con unittest
python -m unittest discover -s tests -p test_*.py -v
```

Inicialmente verás varios tests **SKIPPED** (saltados), lo cual es esperado porque el código aún no está implementado.

### 3. Leer la guía de aprendizaje

```bash
cat LEARNING_GUIDE.md
```

**O mejor**: Abre `LEARNING_GUIDE.md` en tu editor favorito para una mejor lectura con formato.

## 📚 Flujo de Trabajo (TDD)

El enfoque es **Test-Driven Development**:

1. **Lee la teoría** en `LEARNING_GUIDE.md` para la sección que vas a implementar
2. **Examina los tests** en `tests/test_*.py` para entender qué se espera
3. **Ejecuta los tests** para ver cuáles fallan
4. **Implementa las funciones** en `src/*.py` siguiendo los docstrings
5. **Verifica que los tests pasen** ✓
6. **Continúa a la siguiente función**

### Ejemplo: Implementar `compute_image_distance`

```bash
# 1. Leer teoría: LEARNING_GUIDE.md, Sección 1 "Thin Lens Equation"

# 2. Examinar test:
grep -A 10 "def test_compute_image_distance_real_image" tests/test_thin_lens.py

# 3. Ejecutar test (fallará, es lo esperado):
pytest tests/test_thin_lens.py::TestThinLensEquation::test_compute_image_distance_real_image -v

# 4. Implementar función en src/thin_lens.py
# (seguir el docstring como contrato)

# 5. Ejecutar test nuevamente (debe pasar):
pytest tests/test_thin_lens.py::TestThinLensEquation::test_compute_image_distance_real_image -v
```

## 🎯 Implementación Recomendada

### Orden sugerido (por dificultad):

**Fase 1: Thin Lens** (~1-2 horas)
- `compute_image_distance`, `compute_focal_length`, `compute_object_distance`
- `compute_magnification`
- `lens_type`, `image_type`, `image_orientation`

**Fase 2: Transformations** (~2-3 horas)
- Empezar con 2D: `translation_matrix_2d`, `apply_translation_2d`
- Rotación 2D: `rotation_matrix_2d`, `apply_rotation_2d`
- Rotación 3D: `rotation_matrix_3d_x/y/z`, `compose_rotations_3d`
- Transformaciones avanzadas: `affine_matrix_from_points`, `homography_matrix_from_points`

**Fase 3: OpenCV Operations** (~2-3 horas)
- Creación: `create_image`
- Filtros: `apply_blur`, `apply_gaussian_blur`, `apply_median_blur`
- Blending: `blend_images`, `add_weighted_images`
- Brillo/Contraste: `adjust_brightness`, `adjust_contrast`, `adjust_brightness_contrast`
- Histograma: `equalize_histogram_gray`, `equalize_histogram_color`
- Transformaciones: `apply_affine_transform_opencv`, `apply_perspective_transform_opencv`, `rotate_image`

### Monitoreo de progreso

```bash
# Ver cuántos tests pasan en cada módulo
pytest tests/test_thin_lens.py -v --tb=no | tail -1
pytest tests/test_transformations.py -v --tb=no | tail -1
pytest tests/test_opencv_basics.py -v --tb=no | tail -1

# Ver cobertura de código
pytest tests/ --cov=src --cov-report=term-missing

# Ver solo los tests que fallan
pytest tests/ -v --tb=short | grep FAILED
```

## 📝 Notas Importantes

### Para OpenCV

OpenCV en Python se importa como `cv2`:

```python
import cv2
import numpy as np

# Leer imagen
img = cv2.imread("image.jpg")  # Formato BGR (no RGB)

# Convertir color
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Operaciones básicas (ver guía para más)
blurred = cv2.blur(img, (3, 3))
rotated = cv2.warpAffine(img, M, (width, height))
```

Consulta la guía en `LEARNING_GUIDE.md` para ejemplos completos.

### Para Transformaciones

- **Matrices de transformación**: Usar homogéneo (3x3 para 2D, 4x4 para 3D)
- **Aplicar transformación**: 
  - Método 1: `M @ punto_homogéneo` 
  - Método 2: `cv2.warpAffine()` o `cv2.warpPerspective()` para imágenes

### Para Thin Lens

- **Distancias positivas**: objeto y imagen del lado de la lente ("real")
- **Distancias negativas**: imagen del lado opuesto ("virtual")
- **Fórmula**: `1/f = 1/s_o + 1/s_i`

## 🧪 Ejecutar Tests Específicos

```bash
# Un archivo completo
pytest tests/test_thin_lens.py -v

# Una clase de tests
pytest tests/test_thin_lens.py::TestThinLensEquation -v

# Un test específico
pytest tests/test_thin_lens.py::TestThinLensEquation::test_compute_image_distance_real_image -v

# Con salida detallada de errores
pytest tests/test_thin_lens.py -vv --tb=long

# Solo tests que no fueron saltados
pytest tests/ -v -m "not skip"
```

## 🐛 Debugging

Si un test falla:

```bash
# 1. Ejecutar con traceback completo
pytest tests/test_thin_lens.py::TestThinLensEquation::test_compute_image_distance_real_image -vv --tb=long

# 2. Ver exactamente qué valor se esperaba vs. qué se obtuvo
# El mensaje de error te lo mostrará

# 3. Revisar el docstring de la función en src/
# El docstring contiene el "contrato": inputs, outputs, fórmula

# 4. Ejecutar un pequeño script de prueba:
python3 << 'EOF'
import sys
sys.path.insert(0, 'src')
from thin_lens import compute_image_distance
result = compute_image_distance(focal_length=10, object_distance=30)
print(f"Result: {result}, Expected: 15.0")
EOF
```

## 📊 Checklist de Entrega

- [ ] Todos los imports funcionan sin errores
- [ ] Al menos 90% de tests pasan (color verde)
- [ ] No hay `NotImplementedError` al correr tests
- [ ] Código sigue PEP 8 (puedes usar `pycodestyle` para verificar)
- [ ] Docstrings son comprensibles
- [ ] Funciones manejan edge cases (valores cero, negativos, extremos)
- [ ] Ninguna función tiene valores hardcodeados innecesarios

## 🔗 Referencias

- **OpenCV Docs**: https://docs.opencv.org/
- **NumPy Docs**: https://numpy.org/
- **Lab_1.pdf**: Material original del profesor en `/home/work/Develop/Master/CV1/Theory/Lab_1.pdf`
- **LEARNING_GUIDE.md**: Guía completa en este mismo proyecto

## ❓ Preguntas Frecuentes

**P: ¿Puedo modificar los tests?**
No. Los tests son el "especificación" que define qué debe hacer cada función. Modifica solo el código en `src/`.

**P: ¿Qué pasa si un test tiene timeout?**
Probablemente tu función está en un loop infinito. Revisa la lógica.

**P: ¿Necesito numpy para thin_lens?**
No es estrictamente necesario, pero es recomendado para operaciones matemáticas complejas.

**P: ¿Puedo usar funciones de otras librerías?**
Sí, siempre y siempre que uses las librerías de `requirements.txt`. Para `thin_lens.py` evita dependencias externas; para `transformations.py` puedes usar numpy; para `opencv_operations.py` usa cv2 y numpy.

**P: ¿Qué tipo de errores son aceptables?**
Tolerancias de redondeo (`assertAlmostEqual`): sí. Errores lógicos: no.

## 📧 Ayuda

Si tienes problemas:

1. Lee el mensaje de error completo (`-vv --tb=long`)
2. Revisa el docstring de la función
3. Consulta LEARNING_GUIDE.md para la teoría
4. Busca en los tests ejemplos de uso

---

**Creado**: Noviembre 2024  
**Basado en**: Lab_1.pdf, Computer Vision I (Prof. Antonio Rodríguez-Sánchez)  
**Enfoque**: Test-Driven Development (TDD)
