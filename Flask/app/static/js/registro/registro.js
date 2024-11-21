function formatarCPF(input) {
    // Remove qualquer caractere que não seja número
    let valor = input.value.replace(/\D/g, '');

    // Aplica o formato XXX.XXX.XXX-XX
    if (valor.length <= 3) {
        input.value = valor;
    } else if (valor.length <= 6) {
        input.value = valor.replace(/(\d{3})(\d{1,})/, '$1.$2');
    } else if (valor.length <= 9) {
        input.value = valor.replace(/(\d{3})(\d{3})(\d{1,})/, '$1.$2.$3');
    } else {
        input.value = valor.replace(/(\d{3})(\d{3})(\d{3})(\d{1,})/, '$1.$2.$3-$4');
    }
}

// Função para formatar o telefone enquanto o usuário digita
function formatarTelefone(input) {
    // Remove qualquer caractere que não seja número
    let valor = input.value.replace(/\D/g, '');

    // Aplica a formatação (99) 99999-9999
    if (valor.length <= 2) {
        input.value = valor;
    } else if (valor.length <= 6) {
        input.value = `(${valor.slice(0, 2)}) ${valor.slice(2)}`;
    } else {
        input.value = `(${valor.slice(0, 2)}) ${valor.slice(2, 7)}-${valor.slice(7, 11)}`;
    }
}
document.addEventListener('DOMContentLoaded', function () {
    const campos = [
        { id: 'telefone', formatar: formatarTelefone, limite: 15 },
        { id: 'cpf', formatar: formatarCPF, limite: 14 }
    ];

    campos.forEach(campo => {
        const field = document.getElementById(campo.id);
        if (field) {
            field.addEventListener('input', function () {
                campo.formatar(field);
                if (field.value.length > campo.limite) {
                    field.value = field.value.slice(0, campo.limite);
                }
            });
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    flatpickr("#data_nasc", {
        dateFormat: "Y-m-d",  // Define o formato de data
        minDate: "1900-01-01",  // Defina a data mínima, se necessário
        maxDate: "today",  // Limita a seleção de data até o dia de hoje
        altInput: true,  // Exibe o campo de texto alternativo com a data formatada
        altFormat: "F j, Y"  // Formato alternativo, se você quiser exibir a data de forma diferente
    });
});


document.addEventListener('DOMContentLoaded', function() {
    let tipoContaInputs = document.querySelectorAll('input[name="tipo_conta"]');
    tipoContaInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            let tipoConta = this.value;
            // Atualiza o campo hidden com o tipo selecionado
            document.getElementById('tipo_conta').value = tipoConta;
            
            // Mostra ou esconde os campos baseados na seleção
            if (tipoConta === 'usuario') {
                document.getElementById('camposUsuario').style.display = 'block';
                document.getElementById('camposOng').style.display = 'none';
            } else {
                document.getElementById('camposUsuario').style.display = 'none';
                document.getElementById('camposOng').style.display = 'block';
            }
        });
    });
});
