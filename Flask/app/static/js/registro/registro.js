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
function formatarCEP(input) {
    // Remove qualquer caractere que não seja número
    let valor = input.value.replace(/\D/g, '');

    // Aplica o formato XXXXX-XXX
    if (valor.length <= 5) {
        input.value = valor;
    } else {
        input.value = valor.replace(/(\d{5})(\d{1,})/, '$1-$2');
    }

    // Limita o tamanho do valor para 9 caracteres
    if (input.value.length > 9) {
        input.value = input.value.slice(0, 9);
    }
}

function formatarCNPJ(input) {
    // Remove qualquer caractere que não seja número
    let valor = input.value.replace(/\D/g, '');

    // Aplica o formato XX.XXX.XXX/XXXX-XX
    if (valor.length <= 2) {
        input.value = valor;
    } else if (valor.length <= 5) {
        input.value = valor.replace(/(\d{2})(\d{1,})/, '$1.$2');
    } else if (valor.length <= 8) {
        input.value = valor.replace(/(\d{2})(\d{3})(\d{1,})/, '$1.$2.$3');
    } else if (valor.length <= 12) {
        input.value = valor.replace(/(\d{2})(\d{3})(\d{3})(\d{1,})/, '$1.$2.$3/$4');
    } else {
        input.value = valor.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{1,})/, '$1.$2.$3/$4-$5');
    }

    // Limita o tamanho do valor para 18 caracteres
    if (input.value.length > 18) {
        input.value = input.value.slice(0, 18);
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const campos = [
        { id: 'telefone', formatar: formatarTelefone, limite: 15 },
        { id: 'cpf', formatar: formatarCPF, limite: 14 },
        { id: 'cep', formatar: formatarCEP, limite: 9 },
        { id: 'cnpj', formatar: formatarCNPJ, limite: 18 }
    ];

    campos.forEach(campo => {
        const field = document.getElementById(campo.id);
        if (field) {
            field.addEventListener('input', function () {
                campo.formatar(field);
                // Bloquear caracteres além do limite definido
                if (field.value.length > campo.limite) {
                    field.value = field.value.slice(0, campo.limite);
                }
            });
        }
    });
});

function preencherEndereco() {
    const cep = document.getElementById('CEP').value.replace(/\D/g, ''); // Remover tudo o que não for número
    
    if (cep.length === 8) {  // Verifica se o CEP tem 8 dígitos
        fetch(`https://viacep.com.br/ws/${cep}/json/`)
            .then(response => response.json())
            .then(data => {
                if (data.erro) {
                    alert('CEP não encontrado!');
                } else {
                    // Preenche os campos com os dados recebidos
                    document.getElementById('endereco').value = data.logradouro;
                    document.getElementById('bairro').value = data.bairro;
                    document.getElementById('cidade').value = data.localidade;
                    document.getElementById('UF').value = data.uf;
                }
            })
            .catch(error => {
                console.error('Erro ao buscar o CEP:', error);
                alert('Erro ao buscar o CEP.');
            });
    }
}

// Função para formatar o CEP enquanto o usuário digita
function formatarCEP(input) {
    let valor = input.value.replace(/\D/g, '');  // Remove tudo o que não for número
    if (valor.length <= 5) {
        input.value = valor;
    } else {
        input.value = valor.replace(/(\d{5})(\d{1,})/, '$1-$2');
    }
}

// Função para formatar o telefone enquanto o usuário digita
function formatarTelefone(input) {
    let valor = input.value.replace(/\D/g, '');  // Remove tudo o que não for número
    if (valor.length <= 2) {
        input.value = valor;
    } else if (valor.length <= 6) {
        input.value = `(${valor.slice(0, 2)}) ${valor.slice(2)}`;
    } else {
        input.value = `(${valor.slice(0, 2)}) ${valor.slice(2, 7)}-${valor.slice(7, 11)}`;
    }
}

// Função para formatar o CNPJ enquanto o usuário digita
function formatarCNPJ(input) {
    let valor = input.value.replace(/\D/g, '');  // Remove tudo o que não for número
    if (valor.length <= 2) {
        input.value = valor;
    } else if (valor.length <= 5) {
        input.value = valor.replace(/(\d{2})(\d{1,})/, '$1.$2');
    } else if (valor.length <= 8) {
        input.value = valor.replace(/(\d{2})(\d{3})(\d{1,})/, '$1.$2.$3');
    } else if (valor.length <= 12) {
        input.value = valor.replace(/(\d{2})(\d{3})(\d{3})(\d{1,})/, '$1.$2.$3/$4');
    } else {
        input.value = valor.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    flatpickr("#data_nasc", {
        dateFormat: "Y-m-d",  // Define o formato de data
        minDate: "1900-01-01",  // Defina a data mínima, se necessário
        maxDate: "today",  // Limita a seleção de data até o dia de hoje
        altInput: true,  // Exibe o campo de texto alternativo com a data formatada
        altFormat: "F j, Y"  // Formato alternativo, se você quiser exibir a data de forma diferente
    });
});
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
    const inputs = form.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
        if (isActive) {
            input.setAttribute('required', 'required'); // Adiciona 'required'
        } else {
            input.removeAttribute('required'); // Remove 'required'
        }
    });
}


