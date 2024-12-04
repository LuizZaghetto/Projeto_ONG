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
