#!/bin/bash
# monitored_embedded.sh

MEM_LIMIT_KB=65536  # 64MB
STACK_LIMIT_KB=8192 # 8MB

# Aplicar límites
ulimit -v $MEM_LIMIT_KB
ulimit -s $STACK_LIMIT_KB

echo "=== INICIANDO SIMULACIÓN EMBEBIDA ==="
echo "Límites aplicados:"
echo "- RAM máxima: $((MEM_LIMIT_KB / 1024))MB"
echo "- Stack máximo: $((STACK_LIMIT_KB / 1024))MB"

# Ejecutar DIRECTAMENTE el programa
echo "Ejecutando cerradura_simulada..."
./cerradura_inteligente