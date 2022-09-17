const diceId = [
    'dicePlaying1',
    'dicePlaying2',
    'dicePlaying3',
    'dicePlaying4',
    'dicePlaying5',
    'dicePlaying6'
];

let firstPlayerCoords = 0

function randomIntFromInterval(min, max) { // min and max included
  return Math.floor(Math.random() * (max - min + 1) + min)
}

function dicePlaying() {
    document.getElementById('rollDice').style.display = 'none'
    let delay = 100
    let currentIndex = randomIntFromInterval(0, 5)
    let pastIndex
    let interval
    document.getElementById(diceId[currentIndex]).style.display = 'block'
    interval = setInterval(function() {
        pastIndex = currentIndex
        currentIndex = randomIntFromInterval(0, 5)
        currentIndex = (currentIndex === pastIndex) ? (currentIndex + 1) % 6 : currentIndex
        document.getElementById(diceId[currentIndex]).style.display = 'block'
        document.getElementById(diceId[pastIndex]).style.display = 'none'
        }, delay);

    setTimeout(function () {
        clearInterval(interval)
        //alert(currentIndex+1)
        }, 2000)

    setTimeout(function () {
        for (let i = 0; i < 6; i++) {
            document.getElementById(diceId[i]).style.display = 'none'
            document.getElementById('rollDice').style.display = 'block'
        }
        rollDice(firstPlayerCoords, currentIndex + 1)
    }, 3000)
}

function rollDice (index_0, number_steps) {
    const square_cards = [0, 7, 12, 19]
    if (index_0 >= 19) {
        index_0 -= 19
    } else if (index_0 >= 12) {
        index_0 -= 12
    } else if (index_0 >= 7) {
        index_0 -=7
    }
    for (let i = 1; i <= number_steps; i++) {
        if (0 <= firstPlayerCoords && firstPlayerCoords < 7) {
            document.getElementById('firstPlayer').style.left = index_0  * 100 + 200 + 'px'
        } else if (7 <= firstPlayerCoords && firstPlayerCoords < 12) {
            document.getElementById('firstPlayer').style.top = index_0 * 100 + 200 + 'px'
        } else if (12 <= firstPlayerCoords && firstPlayerCoords < 19) {
            if (firstPlayerCoords !== 18){
                document.getElementById('firstPlayer').style.left = 800 - (index_0 * 100 + 100) + 'px'
            } else {
                document.getElementById('firstPlayer').style.left = 800 - (index_0 * 100 + 200) + 'px'
            }
        }
        else {
            if (firstPlayerCoords !== 23){
                document.getElementById('firstPlayer').style.top = 600 - (index_0 * 100 + 100) + 'px'
            } else {
                document.getElementById('firstPlayer').style.top = 600 - (index_0 * 100 + 200) + 'px'
            }
        }

        index_0 ++
        firstPlayerCoords ++
        if (firstPlayerCoords === 24) {
            firstPlayerCoords = 0
        }
        if (square_cards.indexOf(firstPlayerCoords) !== -1) {
            index_0 = 0
        }
    }
    //alert(firstPlayerCoords)
}

//rollDice(firstPlayerCoords, 16)