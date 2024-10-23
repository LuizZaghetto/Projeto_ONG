// Função para carregar o conteúdo do cabeçalho
fetch('../assets-iniciais/header/header.html')
    .then(response => response.text())
    .then(data => {
        document.getElementById('header').innerHTML = data;
    });

// Função para carregar o conteúdo do rodapé
fetch('../assets-iniciais/footer/footer.html')
    .then(response => response.text())
    .then(data => {
        document.getElementById('footer').innerHTML = data;
    });