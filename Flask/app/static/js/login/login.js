function alternarFormularios() {
    const form1 = document.getElementById('form1');
    const form2 = document.getElementById('form2');

    // Alternar visibilidade entre os formulários
    form1.classList.toggle('active');
    form2.classList.toggle('active');

    // Atualizar obrigatoriedade dos campos
    alternarObrigatoriedade(form1, form1.classList.contains('active'));
    alternarObrigatoriedade(form2, form2.classList.contains('active'));
}

function alternarObrigatoriedade(form, isActive) {
    const inputs = form.querySelectorAll('input, select, textarea, button');
    
    inputs.forEach(input => {
        if (isActive) {
            input.removeAttribute('disabled'); // Habilita o campo
            input.setAttribute('required', 'required'); // Adiciona 'required'
        } else {
            input.setAttribute('disabled', 'disabled'); // Desabilita o campo
            input.removeAttribute('required'); // Remove 'required'
        }
    });
}