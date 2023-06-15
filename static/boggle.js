class BoggleGame {
    constructor(boardId, secs = 60) {
        this.secs = secs
        this.showTimer()
        this.score = 0
        this.words = new Set()
        this.board = $("#" + boardId);

        this.timer = setInterval(this.tick.bind(this), 1000)
    }
}