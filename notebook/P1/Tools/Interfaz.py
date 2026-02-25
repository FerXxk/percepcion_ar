import cv2
import numpy as np

def nada(x):
    pass

# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Crear una ventana para los controles
cv2.namedWindow('Controles HSV')
cv2.resizeWindow('Controles HSV', 400, 300)

# Crear trackbars para los rangos HSV
cv2.createTrackbar('H Min', 'Controles HSV', 0, 179, nada)
cv2.createTrackbar('S Min', 'Controles HSV', 0, 255, nada)
cv2.createTrackbar('V Min', 'Controles HSV', 0, 255, nada)
cv2.createTrackbar('H Max', 'Controles HSV', 179, 179, nada)
cv2.createTrackbar('S Max', 'Controles HSV', 255, 255, nada)
cv2.createTrackbar('V Max', 'Controles HSV', 255, 255, nada)

# Crear una ventana para los controles RGB
cv2.namedWindow('Controles RGB')
cv2.resizeWindow('Controles RGB', 400, 300)

# Crear trackbars para los rangos RGB
cv2.createTrackbar('R Min', 'Controles RGB', 0, 255, nada)
cv2.createTrackbar('G Min', 'Controles RGB', 0, 255, nada)
cv2.createTrackbar('B Min', 'Controles RGB', 0, 255, nada)
cv2.createTrackbar('R Max', 'Controles RGB', 255, 255, nada)
cv2.createTrackbar('G Max', 'Controles RGB', 255, 255, nada)
cv2.createTrackbar('B Max', 'Controles RGB', 255, 255, nada)

print("Instrucciones: Ajusta las barras para filtrar colores. Presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # --- PROCESAMIENTO HSV ---
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Leer posiciones de las barras HSV
    hmin = cv2.getTrackbarPos('H Min', 'Controles HSV')
    smin = cv2.getTrackbarPos('S Min', 'Controles HSV')
    vmin = cv2.getTrackbarPos('V Min', 'Controles HSV')
    hmax = cv2.getTrackbarPos('H Max', 'Controles HSV')
    smax = cv2.getTrackbarPos('S Max', 'Controles HSV')
    vmax = cv2.getTrackbarPos('V Max', 'Controles HSV')
    
    lower_hsv = np.array([hmin, smin, vmin])
    upper_hsv = np.array([hmax, smax, vmax])
    mask_hsv = cv2.inRange(hsv, lower_hsv, upper_hsv)
    res_hsv = cv2.bitwise_and(frame, frame, mask=mask_hsv)

    # --- PROCESAMIENTO RGB (en OpenCV es BGR) ---
    # Leer posiciones de las barras RGB
    rmin = cv2.getTrackbarPos('R Min', 'Controles RGB')
    gmin = cv2.getTrackbarPos('G Min', 'Controles RGB')
    bmin = cv2.getTrackbarPos('B Min', 'Controles RGB')
    rmax = cv2.getTrackbarPos('R Max', 'Controles RGB')
    gmax = cv2.getTrackbarPos('G Max', 'Controles RGB')
    bmax = cv2.getTrackbarPos('B Max', 'Controles RGB')
    
    # Nota: OpenCV usa BGR, por lo que el orden en el array es [B, G, R]
    lower_rgb = np.array([bmin, gmin, rmin])
    upper_rgb = np.array([bmax, gmax, rmax])
    mask_rgb = cv2.inRange(frame, lower_rgb, upper_rgb)
    res_rgb = cv2.bitwise_and(frame, frame, mask=mask_rgb)

    # Concatenar resultados para comparar lado a lado
    comparativa = np.hstack((res_hsv, res_rgb))
    
    # Añadir texto a la imagen
    cv2.putText(comparativa, "Filtro HSV", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(comparativa, "Filtro RGB", (frame.shape[1] + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Comparativa HSV vs RGB', comparativa)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()