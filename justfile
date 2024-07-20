dir_growing_islands := 'growing-islands'
dir_diagram_tracer := 'diagram-tracer'

python := env_var_or_default("PYTHON", "python3")
pip := env_var_or_default("PIP", "python3 -m pip")

default:
    @just --list

install-growing-islands:
    {{pip}} install -r {{dir_growing_islands}}/requirements.txt 

install-diagram-tracer:
    {{pip}} install -r {{dir_diagram_tracer}}/requirements.txt

install: install-growing-islands install-diagram-tracer

# Generates a Voronoi diagram
generate-voronoi OUTPUT_FILE NUM_POINTS='32' SEED='0':
    {{python}} {{dir_growing_islands}}/voronoi.py {{OUTPUT_FILE}} --num-points {{NUM_POINTS}} --seed {{SEED}}

# Runs a Voronoi approximation for an input tessellation
run INPUT_FILE:
    {{python}} {{dir_growing_islands}} {{INPUT_FILE}}

# Loads a tessellation from a file and displays it
show INPUT_FILE:
    {{python}} {{dir_growing_islands}}/geometry.py {{INPUT_FILE}}

# Opens the diagram tracing program
open-diagram-tracer INPUT_IMAGE:
    {{python}} {{dir_diagram_tracer}} {{INPUT_IMAGE}}
