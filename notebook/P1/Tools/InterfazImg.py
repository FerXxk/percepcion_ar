import cv2
import numpy as np

def nada(x):
    pass

# 1. CARGAR LA IMAGEN ESTÁTICA
# Cambia 'img1.jpg' por el nombre exacto de tu archivo y su extensión
imagen_original = cv2.imread('../images/Lego.png')

if imagen_original is None:
    print("Error: No se pudo encontrar la imagen 'img1.jpg'. Revisa el nombre y la ruta.")
else:
    # Opcional: Redimensionar si la imagen es muy grande para que quepa en pantalla
    escala = 0.5 # Ajusta este valor (0.5 = 50% del tamaño) si es necesario
    imagen_original = cv2.resize(imagen_original, None, fx=escala, fy=escala)

    # Crear ventana para controles HSV
    cv2.namedWindow('Controles HSV')
    cv2.createTrackbar('H Min', 'Controles HSV', 0, 179, nada)
    cv2.createTrackbar('S Min', 'Controles HSV', 0, 255, nada)
    cv2.createTrackbar('V Min', 'Controles HSV', 0, 255, nada)
    cv2.createTrackbar('H Max', 'Controles HSV', 179, 179, nada)
    cv2.createTrackbar('S Max', 'Controles HSV', 255, 255, nada)
    cv2.createTrackbar('V Max', 'Controles HSV', 255, 255, nada)

    # Crear ventana para controles RGB
    cv2.namedWindow('Controles RGB')
    cv2.createTrackbar('R Min', 'Controles RGB', 0, 255, nada)
    cv2.createTrackbar('G Min', 'Controles RGB', 0, 255, nada)
    cv2.createTrackbar('B Min', 'Controles RGB', 0, 255, nada)
    cv2.createTrackbar('R Max', 'Controles RGB', 255, 255, nada)
    cv2.createTrackbar('G Max', 'Controles RGB', 255, 255, nada)
    cv2.createTrackbar('B Max', 'Controles RGB', 255, 255, nada)

    print("Ajusta los sliders. Presiona 'q' para salir.")

    while True:
        # Hacemos una copia para no sobreescribir la original en cada iteración
        frame = imagen_original.copy()

        # --- PROCESAMIENTO HSV ---
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
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

        # --- PROCESAMIENTO RGB (BGR en OpenCV) ---
        rmin = cv2.getTrackbarPos('R Min', 'Controles RGB')
        gmin = cv2.getTrackbarPos('G Min', 'Controles RGB')
        bmin = cv2.getTrackbarPos('B Min', 'Controles RGB')
        rmax = cv2.getTrackbarPos('R Max', 'Controles RGB')
        gmax = cv2.getTrackbarPos('G Max', 'Controles RGB')
        bmax = cv2.getTrackbarPos('B Max', 'Controles RGB')
        
        lower_rgb = np.array([bmin, gmin, rmin]) # B-G-R
        upper_rgb = np.array([bmax, gmax, rmax])
        mask_rgb = cv2.inRange(frame, lower_rgb, upper_rgb)
        res_rgb = cv2.bitwise_and(frame, frame, mask=mask_rgb)

        # Crear comparativa visual
        comparativa = np.hstack((res_hsv, res_rgb))
        
        cv2.putText(comparativa, "Filtro HSV", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(comparativa, "Filtro RGB", (frame.shape[1] + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow('Comparativa en Imagen Estatica', comparativa)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()