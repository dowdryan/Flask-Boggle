class Game {
    constructor(boardId, seconds) {
        this.seconds = seconds
        this.board = $("#" + boardId);
    }
    countDown() {
        const counter = setInterval(() => {
            if (game.seconds > 0) {
                game.seconds--
                $("#time").html(`<h3 id="time">Time: ${game.seconds}</h3>`)
            } else {
                clearInterval(counter)
                alert("Time's Up.")
                console.log("Time's Up.")
            }
        }, 1000)
    }
}

// $("#score").html(`<p id="score">Score: ${game.score}</p>`)

$("#wordForm").on("submit", function(event) {
    event.preventDefault()
    if (game.seconds <= 0) {
        return
    }
    const wordInput = $("#wordForm input[name='word']").val().trim();
    console.log("wordInput:" + wordInput)

    axios.get("/check_word", {
        params: {
            word: wordInput
        }
    })
    .then(response => {
        if (response.data && response.data.UpdatedScore) {
            const score = response.data.Score;
            $("#score").text(`Score: ${score}`);
        }
    })
    .catch(error => {
        console.error(error);
    });
    $("#wordForm input[name='word']").val(""); // Clear the word input field
})

function updateScore() {
    axios.get("/get_score")
    .then(response => {
        if (response.data && response.data.UpdatedScore) {
            const score = response.data.Score;
            $("#score").text(`Score: ${score}`);
        }
    })
    .catch(error => {
        console.error(error);
    });
}

setInterval(updateScore, 5000);