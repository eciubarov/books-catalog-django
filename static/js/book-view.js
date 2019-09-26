var book_id = document.querySelector('input[name="book_id"]').value
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
function getInitialData() {
    return {
        reviews: [],
        review_object: {
            book: book_id,
            text: null
        },
        is_form_error: false,
        is_loading: false,
        is_responsed: false,
        can_send_request: true,
        form_messages: []
    }
}

var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#book-view',
    data: getInitialData(),
    created: function(){
        this.loadReviews()
    },
    methods: {
        loadReviews() {
            var self = this
            axios.get('/api/reviews/?book_id=' + book_id).then(function(response){
                self.reviews = response.data
            })
        },
        addReview: function() {
            var self = this
            self.is_loading = true
            axios.post('/api/reviews/', self.review_object)
                .then(function (response) {
                    setTimeout(function(){
                        self.is_loading = false
                        if(response.status === 200 || response.status === 201) {
                            self.reviews.push(response.data)
                            self.review_object.text = null
                        } else {
                            alert('Error. Please, contact admin.')
                        }
                    }, 300);
                }).catch(error => {
                    self.is_loading = false
                    if(error.response.status === 400) {
                        alert('Please, fill the text of your review.')
                    }
                });
        },
        reset: function () {
            Object.assign(this.$data, getInitialData())
        }
    }
});