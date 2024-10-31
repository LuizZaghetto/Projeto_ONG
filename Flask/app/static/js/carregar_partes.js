// Função para carregar o conteúdo do cabeçalho
fetch('/header')
    .then(response => response.text())
    .then(data => {
        document.getElementById('header').innerHTML = data;
    });

// Função para carregar o conteúdo do rodapé
fetch('/footer')
    .then(response => response.text())
    .then(data => {
        document.getElementById('footer').innerHTML = data;
    });
