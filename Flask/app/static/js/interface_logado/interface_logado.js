function abrirModal() {
    document.getElementById('modalAdicionarBicho').style.display = 'block';
}

function fecharModal() {
    document.getElementById('modalAdicionarBicho').style.display = 'none';
}

// Fecha o modal ao clicar fora dele
window.onclick = function(event) {
    const modal = document.getElementById('modalAdicionarBicho');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};
