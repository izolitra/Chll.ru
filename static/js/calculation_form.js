const showPopupBtns = document.getElementsByClassName('showPopup')
const popups = document.getElementsByClassName('popup')
const closeBtns = document.getElementsByClassName('close-button')
const popupOverlays = document.getElementsByClassName('popup-overlay');
const popupContents = document.getElementsByClassName('popup-content');


function showPopup(popupNumber) {
  for (let popup of popups) {
    if (popup.dataset.popup === popupNumber) {
      popup.style.display = 'block';
    }
  }
  let overlay = document.querySelector('.popup-overlay');
  overlay.classList.add('overlay-visible'); // Добавить класс для показа затемнения
  overlay.style.display = 'block'; // Показать затемнение
}

function hidePopups() {
  for (let popup of popups) {
    popup.style.display = 'none';
  }
  let overlay = document.querySelector('.popup-overlay');
  overlay.classList.remove('overlay-visible'); // Удалить класс для скрытия затемнения
  overlay.style.display = 'none'; // Скрыть затемнение
}

for (let showPopupBtn of showPopupBtns) {
  showPopupBtn.addEventListener('click', function(e) {
    showPopup(showPopupBtn.dataset.popup)
  })
}

for (let closeBtn of closeBtns) {
  closeBtn.addEventListener('click', function(e) {
    hidePopups()
  })
}

for (let popupOverlay of popupOverlays) {
  popupOverlay.addEventListener('click', function(e) {
    console.log('asdasdsa')
    hidePopups()
  })
}

// for (let popupContent of popupContents) {
//   popupContent.addEventListener('click', function(e) {
//     hidePopups()
//   })
// }