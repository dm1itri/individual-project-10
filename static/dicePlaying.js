const diceId = [
    'dicePlaying1',
    'dicePlaying2',
    'dicePlaying3',
    'dicePlaying4',
    'dicePlaying5',
    'dicePlaying6'
];
const countPlayers = 4
let firstPlayerCoords
let secondPlayerCoords
let thirdPlayerCoords
let fourthPlayerCoords
const playersCoords = [firstPlayerCoords, secondPlayerCoords, thirdPlayerCoords, fourthPlayerCoords]
const rusNamePlayers = ['желтый', 'зеленый', 'красный', 'синий']
const enNamePlayers = ['yellow', 'green', 'red', 'blue']
let currentPlayer
const gameID = 1

function randomIntFromInterval(min, max) { // min and max included
  return Math.floor(Math.random() * (max - min + 1) + min)
}


function getCurrentPlayer(url) {
    var xhr = new XMLHttpRequest()
    let currPlayer
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
        currPlayer = JSON.parse(xhr.response)
        }
    }

    xhr.open('GET', url, false)
    xhr.send()
    return currPlayer[`${gameID}`]['current_player']
}


function putCurrentPLayer(url, skipMove) {
    let data = new FormData()
    data.append('current_player',  currentPlayer + 1)
    data.append('current_position', playersCoords[currentPlayer])
    data.append('skipping_move', skipMove)
    var xhr = new XMLHttpRequest()
    xhr.open('PUT', url, false)
    xhr.send(data)
}

function getCurrentPlayers(url) {
    var xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
        games_args = JSON.parse(xhr.response)
        }
    }

    xhr.open('GET', url, false)
    xhr.send()
    currentPlayer = games_args['current_player']
    firstPlayerCoords = games_args['first_player']['current_position']
    secondPlayerCoords = games_args['second_player']['current_position']
    thirdPlayerCoords = games_args['third_player']['current_position']
    fourthPlayerCoords = games_args['fourth_player']['current_position']
    if (firstPlayerCoords !== 0) {rollDice(0, 0, firstPlayerCoords)}
    if (secondPlayerCoords !== 0) {rollDice(1, 0, secondPlayerCoords)}
    if (thirdPlayerCoords !== 0) {rollDice(2, 0, thirdPlayerCoords)}
    if (fourthPlayerCoords !== 0) {rollDice(3, 0, fourthPlayerCoords)}

}

getCurrentPlayers(`http://127.0.0.1:5000/api/players/${gameID}`)


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
        }, 2000)

    setTimeout(function () {
        for (let i = 0; i < 6; i++) {
            document.getElementById(diceId[i]).style.display = 'none'
            document.getElementById('rollDice').style.display = 'block'
        }
        move(currentPlayer, currentIndex + 1)
        // rollDice(currentPlayer, playersCoords[currentPlayer], currentIndex + 1)
    }, 3000) // 3000
}

function rollDice (numberPlayer, index_0, number_steps) {
    const square_cards = [0, 7, 12, 19]
    const playerId = ['firstPlayer', 'secondPlayer', 'thirdPlayer', 'fourthPlayer']
    let coords
    let realCoords = index_0
    //const pos_x0 = [200, 100, 200]
    //const pos_y0 = [200, 100, 200]
    //const pos_x1 = [100, 100, 200]
    //const pos_y1 = [200, 100, 200]
    let move
    if (index_0 >= 19) {
        index_0 -= 19
    } else if (index_0 >= 12) {
        index_0 -= 12
    } else if (index_0 >= 7) {
        index_0 -=7
    }

    for (let i = 1; i <= number_steps; i++) {
        coords = realCoords
        if (numberPlayer === 0) {
            if (0 <= coords && coords < 7 || 12 <= coords && coords < 19) {
                if (0 <= coords && coords< 7) {
                    move =  index_0  * 100 + 200
                } else {
                    move = coords !== 18 ? 700 - index_0 * 100 : 700 - index_0 * 100 - 100
                }
                document.getElementById(playerId[numberPlayer]).style.left = move + 'px'
            } else {
                if (7 <= coords && coords < 12) {
                    move = index_0 * 100 + 200
                } else {
                    move = coords !== 23 ? 500 - index_0 * 100 : move = 500 - index_0 * 100 - 100
                }
                document.getElementById(playerId[numberPlayer]).style.top = move + 'px'
            }
        } else if (numberPlayer === 1) {
            if (0 <= coords && coords < 7 || 12 <= coords && coords < 19) {
                if (0 <= coords && coords < 7) {
                    move =  coords !== 6 ? index_0  * 100 + 250 : index_0  * 100 + 350
                } else {
                    move =  750 - index_0 * 100
                }
                document.getElementById(playerId[numberPlayer]).style.left = move + 'px'
            } else {
                if (7 <= coords && coords < 12) {
                    move = index_0 * 100 + 200
                } else {
                    move = coords !== 23 ? 500 - index_0 * 100: move = 500 - index_0 * 100 - 100
                }
                document.getElementById(playerId[numberPlayer]).style.top = move + 'px'
            }
        } else if (numberPlayer === 2) {
            if (0 <= coords && coords < 7 || 12 <= coords && coords < 19) {
                if (0 <= coords && coords < 7) {
                    move =  index_0  * 100 + 200
                } else {
                    move = coords !== 18 ? 700 - index_0 * 100 : 700 - index_0 * 100 - 100
                }
                document.getElementById(playerId[numberPlayer]).style.left = move + 'px'
            } else {
                if (7 <= coords && coords < 12) {
                    move = coords !== 11 ? index_0 * 100 + 250 : index_0 * 100 + 350
                } else {
                    move =  550 - index_0 * 100
                }
                document.getElementById(playerId[numberPlayer]).style.top = move + 'px'
            }
        } else if (numberPlayer === 3) {
            if (0 <= coords && coords < 7 || 12 <= coords && coords < 19) {
                if (0 <= coords && coords < 7) {
                    move = coords !== 6 ? index_0  * 100 + 250 : index_0  * 100 + 350
                } else {
                    move =  750 - index_0 * 100
                }
                document.getElementById(playerId[numberPlayer]).style.left = move + 'px'
            } else {
                if (7 <= coords && coords < 12) {
                    move = coords !== 11 ? index_0 * 100 + 250 : index_0 * 100 + 350
                } else {
                    move =  550 - index_0 * 100
                }
                document.getElementById(playerId[numberPlayer]).style.top = move + 'px'
            }
        }

        index_0 ++
        realCoords = realCoords === 23 ? 0 : realCoords + 1
        if (square_cards.indexOf(realCoords) !== -1) {
            index_0 = 0
        }
    }
    return realCoords
}


function checkSquareCards(numberPlayer) {
    if (playersCoords[numberPlayer] === 12) {
        countSteps = randomIntFromInterval(1, 23)
        setTimeout(rollDice, 1000, numberPlayer, playersCoords[numberPlayer], countSteps)
        playersCoords[numberPlayer] = (countSteps + playersCoords[numberPlayer]) % 24
    }
    if (playersCoords[numberPlayer] === 19) {
        setTimeout(rollDice, 2000, numberPlayer, playersCoords[numberPlayer], 12)
        // 2000 таймаут поставлен, т.к. если попадет сюда с телепорта, то не будет видно перемещение сюда, а сразу в парк
        playersCoords[numberPlayer] = 7
    }
    if (playersCoords[numberPlayer] === 7) {
        return 1
    }
    return 0

}

/*
основная функия, отвечающая за вызов:
функции перемещения фигурок,
функции проверки попадания на особенные карточки,
проверки списка спящих,
информаирования кто ходит
 */
function move(numberPlayer, number_steps) {

    playersCoords[numberPlayer] = rollDice(numberPlayer, playersCoords[numberPlayer], number_steps)
    putCurrentPLayer(`http://127.0.0.1:5000/api/game/${gameID}`, checkSquareCards(numberPlayer))

    currentPlayer = getCurrentPlayer(`http://127.0.0.1:5000/api/game/${gameID}`)

    document.getElementById("numberPlayer").innerText = rusNamePlayers[currentPlayer]
    document.getElementById("numberPlayer").style.color = enNamePlayers[currentPlayer]
    console.log(playersCoords)
}