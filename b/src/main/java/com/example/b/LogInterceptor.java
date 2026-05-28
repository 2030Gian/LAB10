package com.example.b;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Component
public class LogInterceptor implements HandlerInterceptor {

    private static final Logger logger = LoggerFactory.getLogger(LogInterceptor.class);
    private static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm");

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        // Marcamos el tiempo de inicio
        request.setAttribute("startTime", System.currentTimeMillis());
        return true;
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) {
        long startTime = (Long) request.getAttribute("startTime");
        long endTime = System.currentTimeMillis();
        long latency = endTime - startTime; // Latencia calculada

        String fecha = LocalDateTime.now().format(formatter);
        String modulo = "SearchAPI"; // Cambiar según el microservicio
        String api = request.getRequestURI();
        String funcion = request.getMethod();
        int status = response.getStatus();

        // Nomenclatura exacta solicitada: {Fecha}{Modulo}{API}{Funcion} Message
        // Guardamos el status y la latencia en el mensaje para que el Bot lo lea en la Parte II
        String logMessage = String.format("{%s}{%s}{%s}{%s} Status:%d Latency:%dms",
                fecha, modulo, api, funcion, status, latency);

        logger.info(logMessage);
    }
}