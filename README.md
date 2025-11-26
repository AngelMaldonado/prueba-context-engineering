# Prueba técnica Context Engineering

## Descripción

Para aplicar al puesto deberás hacer la implementación de un proyecto de software. El ámbito queda completamente a tu criterio, pero deberás cumplir con los siguientes requisitos:

- Tener backend + frontend (puede ser UI en web o una utilidad CLI)
- Fácil de instalar y ejecutar en local (ver la sección de Instalación)
- Variables de entorno en un archivo `.env` en caso de requerir configuración adicional
- Logging de errores y eventos importantes
- Hacer commits atómicos y con mensajes descriptivos de cada iteración o cambio importante para ver el progreso del proyecto.
- Al menos una funcionalidad que utilice inteligencia artificial, como por ejemplo:
  - Resumen de un texto
  - Chat con un modelo de IA
  - Explicación de datos o información

Recursos para ideas de proyectos:

- [The-Tool-Coders](https://github.com/The-Cool-Coders/Project-Ideas-And-Resources)
- [florinpop17/app-ideas](https://github.com/florinpop17/app-ideas)
- [Build Your Own X](https://github.com/codecrafters-io/build-your-own-x)
- [Roadmap.sh](https://roadmap.sh/)
- [Awesome Self Hosted](https://github.com/awesome-selfhosted/awesome-selfhosted)

**IMPORTANTE:** Deberás aplicar CONTEXT ENGINEERING para el desarrollo del proyecto. Revisa este recurso para entender de qué se trata:

[Context Engineering](https://www.youtube.com/watch?v=Egeuql3Lrzg)

En este repositorio ya está la estructura base de las carpetas para aplicar el Context Engineering.

> **Nota:** En el video se usa **Claude Code**, pero puedes utilizar cualquier herramienta de IA que se menciona más adelante, simplemente debes mencionar los archivos en el prompt.
>
> Para la inicialización del proyecto es importante que dejes la estructura de las carpetas y archivos base. La IA solo deberá entender tus requerimientos y trabajar sobre la base que ya hiciste.

## Tecnologías

**IMPORTANTE:** Para la aplicación de Context Engineering, deberás utilizar al menos una de las siguientes herramientas:

- **Claude Code**
- **Codex**
- **Gemini CLI** (gratis)
- **Antigravity** (gratis)
- **Cursor**
- **Zed** (gratis)

Si decides utilizar **Cursor**, **Antigravity** o **Zed**, deberás utilizar las características de programación "Agéntica" para validar la aplicación de Context Engineering, no solamente el autocompletado. Generalmente hay una pestaña "Agents" que te permite crear un agente que te ayude a desarrollar el proyecto.

### Lenguajes de programación

Deberás utilizar al menos uno de los siguientes lenguajes de programación:

- **Python**
- **JavaScript** (preferible **TypeScript**)

### Frameworks

Deberás utilizar al menos uno de los siguientes frameworks:

- **FastAPI**
- **Django**
- **Express**
- **Hono**
- **NextJS**
- **SvelteKit**

## Instalación

Se espera que tu proyecto sea fácil de instalar y ejecutar en local.

### Python

```bash
pip install -r requirements.txt
python main.py
```

O alternativamente:

```bash
uv run main.py
```

### JavaScript/TypeScript

```bash
npm install
npm run start
```

## Pasos para aplicar

1. Haz un fork de este repositorio.
2. Clona el repositorio localmente.
3. Haz el desarrollo de tu proyecto.
4. Agrega tu cv en la carpeta `docs/`
5. Crea un pull request indicando:
   - Nombre del proyecto.
   - Tu nombre.
   - Descripción del proyecto.
   - Pasos de instalación y ejecución.
