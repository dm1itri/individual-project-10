const diceId = [
    'dicePlaying1',
    'dicePlaying2',
    'dicePlaying3',
    'dicePlaying4',
    'dicePlaying5',
    'dicePlaying6'
];
const questionCards = [1, 2, 3, 4, 5, 6, 8, 10, 11, 13, 14, 15, 16, 17, 18, 20, 22, 23]
const questionBiologyCards = [2, 3, 10, 14, 17, 22]
const questionHistoryCards = [1, 5, 11, 15, 18, 23]
//const questionGeographyCards = [4, 6, 8, 13, 16, 20]
//const questionBiologyCards = [3, 4, 11, 15, 18, 23]
//const questionHistoryCards = [2, 6, 12, 16, 19, 24]
const rusNamePlayers = ['желтый', 'зеленый', 'красный', 'синий']
const enNamePlayers = ['yellow', 'green', 'red', 'blue']
let answerCorrect
let currentPlayer
// const gameID = parseInt(document.location.pathname.substring(6))
let playersCoords = []
// let playersPoints
let thinksAboutTheQuestion
let thisPlayer = Number(document.cookie.match(/number_move=(.+?)(;|$)/)[1])
let numberHistory


function getCurrentPlayer() {
    let xhr = new XMLHttpRequest()
    let currPlayer
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                currPlayer = JSON.parse(xhr.response)
            }
            else {
                console.log(xhr.status)
            }
        }
    }
    xhr.open('GET', `http://127.0.0.1:5000/api/game`, false)
    xhr.send()
    return currPlayer
}
function putCurrentPLayer(skipMove, currentPlayer, playerCoords, numberOfPoints, thinksAboutTheQuestion) {
    let data = new FormData()
    data.append('current_player',  currentPlayer)
    data.append('current_position', playerCoords)
    data.append('skipping_move', skipMove)
    data.append('number_of_points', numberOfPoints)
    data.append('thinks_about_the_question', thinksAboutTheQuestion)
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status !== 200) {
            console.log(xhr.status)
        }
    }
    xhr.open('PUT', `http://127.0.0.1:5000/api/game`, false)
    xhr.send(data)
}
function putHistoryMove(currentPlayer, numberSteps) {
    let data = new FormData()
    data.append('number_move',  currentPlayer)
    data.append('number_steps', numberSteps)
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status !== 200) {
                console.log(xhr.status)
        }
    }
    xhr.open('PUT', `http://127.0.0.1:5000/api/history_game`, false)
    xhr.send(data)
}
function getHistoryMove(numberHistory) {
    let xhr = new XMLHttpRequest()
    let history
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                history = JSON.parse(xhr.response)
            } else {
                history = null
        }
    }
    xhr.open('GET', `http://127.0.0.1:5000/api/history_game?number_history=${numberHistory}`, false)
    xhr.send()
    return history
}
function getQuestion(typeQuestion=null, questionId=null) {
    let xhr = new XMLHttpRequest()
    let question
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if  (xhr.status === 200) {
                question = JSON.parse(xhr.response)
            }
            else {
                console.log(xhr.status)
            }
        }
    }
    xhr.open('GET', `http://127.0.0.1:5000/api/question?type_question=${typeQuestion}&question_id=${questionId}`, false)
    xhr.send()
    return question
}
function getCurrentPlayers() {
    let games_args
    let xhr = new XMLHttpRequest()

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            games_args = JSON.parse(xhr.response)
        }
    }

    xhr.open('GET', `http://127.0.0.1:5000/api/players`, false)
    xhr.send()
    currentPlayer = games_args['current_player']
    numberHistory = games_args['number_history']
    for (let i = 0; i < games_args['count_players']; i++){
        playersCoords.push(games_args[`${i}_player`]['current_position'])
        document.getElementById(`${i}_Player`).style.display = 'block'
        if (playersCoords[i] !== 0) {rollDice(i, 0, playersCoords[i])}
    }
    if (games_args['question_id'] !== null) {
        answerCorrect = updateQuestion(getQuestion(null, games_args['question_id']))
    }
    return games_args[`${thisPlayer}_player`]['thinks_about_the_question']
}

const randomIntFromInterval = (min, max) => Math.floor(Math.random() * (max - min + 1) + min) // min and max included


async function dicePlaying() {
    document.getElementById('buttonDicePlaying').style.visibility = 'hidden'
    let delay = 100
    let numberSteps = randomIntFromInterval(0, 5)
    let pastIndex
    let interval
    document.getElementById(diceId[numberSteps]).style.display = 'block'
    interval = setInterval(function() {
        pastIndex = numberSteps
        numberSteps = randomIntFromInterval(0, 5)
        numberSteps = (numberSteps === pastIndex) ? (numberSteps + 1) % 6 : numberSteps
        document.getElementById(diceId[numberSteps]).style.display = 'block'
        document.getElementById(diceId[pastIndex]).style.display = 'none'
        }, delay);

    setTimeout(() => clearInterval(interval), 2000)
    setTimeout(function () {
        document.getElementById(diceId[numberSteps]).style.display = 'none'
        move(currentPlayer, numberSteps + 1)
        // rollDice(currentPlayer, playersCoords[currentPlayer], currentIndex + 1)
    }, 3000) // 3000
}

function rollDice (numberPlayer, index_0, number_steps) {
    const square_cards = [0, 7, 12, 19]
    let realCoords = index_0
    let move
    if (index_0 >= 19) {
        index_0 -= 19
    } else if (index_0 >= 12) {
        index_0 -= 12
    } else if (index_0 >= 7) {
        index_0 -=7
    }

    for (let i = 1; i <= number_steps; i++) {
        if (0 <= realCoords && realCoords < 7) {
            if (numberPlayer % 2) {
                move =  realCoords !== 6 ? index_0  * 100 + 250 : index_0  * 100 + 350
            } else {
                move =  index_0  * 100 + 200
            }
            document.getElementById(`${numberPlayer}_Player`).style.left = move + 'px'
        } else if (7 <= realCoords && realCoords < 12) {
            if (numberPlayer < 2) {
                move = index_0 * 100 + 200
            } else {
                move = realCoords !== 11 ? index_0 * 100 + 250 : index_0 * 100 + 350
            }
            document.getElementById(`${numberPlayer}_Player`).style.top = move + 'px'
        } else if (12 <= realCoords && realCoords < 19) {
            if (numberPlayer % 2) {
                move =  750 - index_0 * 100
            } else {
                move = realCoords !== 18 ? 700 - index_0 * 100 : 700 - index_0 * 100 - 100
            }
            document.getElementById(`${numberPlayer}_Player`).style.left = move + 'px'
        } else {
            if (numberPlayer < 2) {
                move = realCoords !== 23 ? 500 - index_0 * 100 : 500 - index_0 * 100 - 100
            } else {
                move = 550 - index_0 * 100
            }
            document.getElementById(`${numberPlayer}_Player`).style.top = move + 'px'
        }
        realCoords = realCoords === 23 ? 0 : realCoords + 1
        index_0 = square_cards.includes(realCoords) ? 0: index_0 + 1
    }
    return realCoords
}


function checkSquareCards(numberPlayer) {
    if (playersCoords[numberPlayer] === 12) {
        let countSteps = randomIntFromInterval(1, 23)
        setTimeout(rollDice, 1000, numberPlayer, playersCoords[numberPlayer], countSteps)
        putHistoryMove(currentPlayer, countSteps)
        playersCoords[numberPlayer] = (countSteps + playersCoords[numberPlayer]) % 24
        numberHistory += 1
    }
    if (playersCoords[numberPlayer] === 19) {
        setTimeout(rollDice, 2000, numberPlayer, playersCoords[numberPlayer], 12)
        // 2000 таймаут поставлен, т.к. если попадет сюда с телепорта, то не будет видно перемещение сюда, а сразу в парк
        putHistoryMove(currentPlayer, 12)
        playersCoords[numberPlayer] = 7
        numberHistory += 1
    }
    if (playersCoords[numberPlayer] === 7) {
        return 1
    }
    return 0
}


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


function updateDocument(currentPlayer, thinksAboutTheQuestion=false) {
    document.getElementById("numberPlayer").innerText = rusNamePlayers[currentPlayer]
    document.getElementById("numberPlayer").style.color = enNamePlayers[currentPlayer]
    document.getElementById("buttonDicePlaying").style.visibility = (currentPlayer === thisPlayer && !thinksAboutTheQuestion) ? 'visible' : 'hidden'
}

function updateQuestion(question) {
    const answerCorrect = randomIntFromInterval(1, 4)
    document.getElementById("question_1").innerText = question['question']
    for (let i=2; i < 5; i++) {
        document.getElementById(`btn_answer_${i}`).value = question[`answer_${i}`]
    }
    if (answerCorrect !== 1) {
        document.getElementById(`btn_answer_1`).value = question[`answer_${answerCorrect}`]
    }
    document.getElementById(`btn_answer_${answerCorrect}`).value = question[`answer_correct`]
    document.getElementById("question").style.visibility = 'visible'
    return answerCorrect
}


async function choosingAnswer(numberChoosingAnswer) {
    let point = 1
    console.log(answerCorrect)
    document.getElementById(`btn_answer_${answerCorrect}`).style.background = 'rgba(0,255,0,0.71)'
    if (numberChoosingAnswer !== answerCorrect) {
        point = 0
        document.getElementById(`btn_answer_${numberChoosingAnswer}`).style.background = 'rgba(255,0,0,0.89)'
    }
    setTimeout(function () {
        document.getElementById(`btn_answer_${answerCorrect}`).style.background = 'buttonface'
        document.getElementById(`btn_answer_${numberChoosingAnswer}`).style.background = 'buttonface'
        document.getElementById("question").style.visibility = 'hidden'
    }, 3000)
    await endMoveAndAnswer(currentPlayer, playersCoords[currentPlayer] === 7 ? 1 : 0, playersCoords[currentPlayer], point, false)
}

async function move(numberPlayer, numberSteps) {
    let question
    putHistoryMove(numberPlayer, numberSteps)
    numberHistory += 1
    playersCoords[numberPlayer] = rollDice(numberPlayer, playersCoords[numberPlayer], numberSteps)
    let skippingMove = checkSquareCards(numberPlayer)
    if (skippingMove === 0 && playersCoords[numberPlayer] in questionCards ) {
        endMoveAndAnswer(numberPlayer, skippingMove, playersCoords[numberPlayer], 0, true)
        if (questionBiologyCards.includes(playersCoords[numberPlayer])){
            question = getQuestion('Биология')
        } else if (questionHistoryCards.includes(playersCoords[numberPlayer])) {
            question = getQuestion('История')
        } else {
            question = getQuestion('География')
        }
        answerCorrect = updateQuestion(question)
    }
    else {
        endMoveAndAnswer(numberPlayer, skippingMove, playersCoords[numberPlayer], 0, false)
    }
}

async function endMoveAndAnswer(numberPlayer, skipMove, playerCoords, numberOfPoints, thinksAboutTheQuestion) {
    putCurrentPLayer(skipMove, numberPlayer, playerCoords, numberOfPoints, thinksAboutTheQuestion)
    //currentPlayer = getCurrentPlayer()['current_player']
    //updateDocument(currentPlayer, thinksAboutTheQuestion)
    if (!thinksAboutTheQuestion) {
        await waiting_move()
    }
}

async function waiting_move() {
    let numberMove, result, nextHistory
    let t = true
    while (t) {
        result = getCurrentPlayer()
        currentPlayer = result['current_player']
        nextHistory = getHistoryMove(numberHistory + 1)
        updateDocument(currentPlayer, result['thinks_about_the_question'] && currentPlayer === thisPlayer)
        if (currentPlayer === thisPlayer && nextHistory === null) {
            t = false
        } else if (nextHistory === null) {
            await sleep(2000)
        } else {
            numberMove = nextHistory['number_move']
            playersCoords[numberMove] = rollDice(numberMove, playersCoords[numberMove], nextHistory['number_steps'])
            numberHistory += 1
            await sleep (2000)
        }
    }
}

thinksAboutTheQuestion = getCurrentPlayers()
updateDocument(currentPlayer, thinksAboutTheQuestion)
waiting_move()