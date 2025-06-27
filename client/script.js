const dom = document.querySelector('.search');


const eventClick = async () => {
  const inputVal = document.querySelector('.item')
  const listaItem = document.querySelector('.lista_itens')
  listaItem.textContent = ''
  const url = `http://localhost:3000/busca/${inputVal.value}`

  try {
    const response = await fetch(url, {
      headers: {
        "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
       
        "User-Agent":  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Pragma": 'no-cache',
        "TE": 'Trailers',
        'Upgrade-Insecure-Requests':1
    }
    });
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const resultado = await response.json()

    resultado.forEach((data) => {
      console.log(data)
      const li = document.createElement('li')
      const img = document.createElement('img')
      const span = document.createElement('span')
      listaItem.appendChild(li)
      li.appendChild(span)
      span.textContent = data.name
      li.appendChild(img)
      img.src = data.img
    })

  } catch (error) {
    console.error(error.message);
  }
}

dom.addEventListener('click', eventClick)