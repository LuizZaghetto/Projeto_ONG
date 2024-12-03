console.log('test')

const user_id = 10 // Logica para pegar o id do usuario logado

const likedBtn = document.querySelector('#gostei')
const dislikedBtn = document.querySelector('#passar')

async function setResponse() {
    const animal = document.querySelector('#current-card')
    const animal_id = animal.dataset.currentId
    await fetch('http://localhost:3001/doginder', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id, animal_id, isLiked }),
    });
}

let isLiked = ''

likedBtn.addEventListener('click', async (e) => {
    e.preventDefault()
    isLiked = true
    await setResponse()

})

dislikedBtn.addEventListener('click', async () => {
    console.log('teste 2')
    isLiked = false
    await setResponse()
})

