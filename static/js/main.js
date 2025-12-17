document.addEventListener('DOMContentLoaded', () => {
    const slidesContainer = document.querySelector('.slides')
    const slides = document.querySelectorAll('.slides img')
    const prevBtn = document.querySelector('.prev')
    const nextBtn = document.querySelector('.next')

    let index = 0
    const total = slides.length

    function showSlide(i) {
        slidesContainer.style.transform = `translateX(${-i * 100}%)`
    }

    // Автопрокрутка
    let slideInterval = setInterval(() => {
        index = (index + 1) % total
        showSlide(index)
    }, 5000)

    // Кнопки вручную
    prevBtn.addEventListener('click', () => {
        index = (index - 1 + total) % total
        showSlide(index)
        resetInterval()
    })

    nextBtn.addEventListener('click', () => {
        index = (index + 1) % total
        showSlide(index)
        resetInterval()
    })

    function resetInterval() {
        clearInterval(slideInterval)
        slideInterval = setInterval(() => {
            index = (index + 1) % total
            showSlide(index)
        }, 3000)
    }
})