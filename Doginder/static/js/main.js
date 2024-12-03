document.addEventListener('DOMContentLoaded', () => {
    let id = 1
    const cardContainer = document.getElementById('card-container');
    const passarBtn = document.getElementById('passar');
    const gosteiBtn = document.getElementById('gostei');

    passarBtn.addEventListener('click', () => handleSwipe('passar'));
    gosteiBtn.addEventListener('click', () => handleSwipe('gostei'));

    function handleSwipe(action) {
        const currentCard = document.getElementById('current-card');
        currentCard.style.transition = 'transform 0.5s ease, opacity 0.5s ease';
        currentCard.style.transform = action === 'gostei' ? 'translateX(100%)' : 'translateX(-100%)';
        currentCard.style.opacity = '0';

        setTimeout(() => {
            cardContainer.removeChild(currentCard);
            loadNextCard();
        }, 500);
    }

    function loadNextCard() {
        // Aqui você pode carregar o próximo perfil via API ou backend.
        const newCard = document.createElement('div');
        newCard.className = 'card';
        newCard.id = 'current-card';
        newCard.dataset.currentId = ++id
        newCard.innerHTML = `
            <img src="URL_DA_NOVA_IMAGEM" alt="Foto do animal">
            <h2>Nome do Novo Perfil</h2>
            <p>Descrição do novo perfil.</p>
        `;
        cardContainer.appendChild(newCard);
    }
});
