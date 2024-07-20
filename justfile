dir_growing_islands := 'growing_islands'
dir_tessellation_tracer := 'tessellation_tracer'

python := env_var_or_default("PYTHON", "python3")
pip := env_var_or_default("PIP", "python3 -m pip")

default:
    @just --list

install-growing-islands:
    {{pip}} install -r {{dir_growing_islands}}/requirements.txt 

install-tessellation-tracer:
    {{pip}} install -r {{dir_tessellation_tracer}}/requirements.txt

install: install-growing-islands install-tessellation-tracer

# Generates a Voronoi tessellation
generate-voronoi OUTPUT_FILE NUM_POINTS='32' SEED='0':
    {{python}} {{dir_growing_islands}}/voronoi.py {{OUTPUT_FILE}} --num-points {{NUM_POINTS}} --seed {{SEED}}

# Runs a Voronoi approximation for an input tessellation
run INPUT_FILE:
    {{python}} {{dir_growing_islands}} {{INPUT_FILE}}

# Loads a tessellation from a file and displays it
show INPUT_FILE:
    {{python}} {{dir_growing_islands}}/geometry.py {{INPUT_FILE}}

# Opens the tessellation tracer program
open-tessellation_tracer INPUT_IMAGE:
    {{python}} {{dir_tessellation_tracer}} {{INPUT_IMAGE}}
