package com.example.b;

import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
@RequestMapping("/poke")
public class SearchController {

    @PostMapping("/search")
    public Object searchPokemon(@RequestBody Map<String, String> request) {
        String pokemonName = request.get("Pokemon_Name");

        // TODO: Aquí llamaremos a la POKE API externa y a los otros servicios.

        return Map.of(
                "name", pokemonName != null ? pokemonName : "unknown",
                "stats", "[]", // Placeholder
                "image", "/url-placeholder" // Placeholder
        );
    }
}