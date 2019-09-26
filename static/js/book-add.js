var is_edit = parseInt(document.querySelector('input[name="is_edit"]').value),
    book_id = parseInt(document.querySelector('input[name="book_id"]').value)
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
function getInitialData() {
    return {
        is_edit: !!is_edit,
        book_id: book_id,
        cover: '',
        cover_loading: false,
        author: {
            first_name: '',
            last_name: ''
        },
        category: {
            name: ''
        },
        cover_object: {
            id: null,
            url: null,
            thumbnail: null
        },
        book_object: {
            id: null,
            title: '',
            description: '',
            authors: [],
            categories: [],
            cover: null
        },
        authors: [],
        categories: [],
        is_form_error: false,
        is_loading: false,
        is_responsed: false,
        can_send_request: true,
        form_messages: []
    }
}

var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#add-book',
    data: getInitialData(),
    created: function(){
        this.loadAuthors()
        this.loadCategories()
        if(this.is_edit) {
            this.loadBook()
        }
    },
    methods: {
        loadBook() {
            var self = this
            axios.get('/api/books/' + self.book_id + '/').then(function(response){
                self.book_object = response.data
                axios.get('/api/covers/' + response.data.cover + '/').then(function(response){
                    self.cover_object = response.data
                })
            })

        },
        addAuthor() {
            var self = this
            if(this.author.first_name !== '' && this.author.last_name !== '') {
                let formData = new FormData()
                formData.append('first_name', this.author.first_name)
                formData.append('last_name', this.author.last_name)
                axios.post('/api/authors/', formData).then(function(){
                    self.author.first_name = ''
                    self.author.last_name = ''
                    self.loadAuthors()
                })
            } else {
                alert('Please, fill author first name and last name.')
            }
        },
        addCategory() {
            var self = this
            if(this.category.name !== '') {
                let formData = new FormData()
                formData.append('name', this.category.name)
                axios.post('/api/categories/', formData).then(function(){
                    self.category.name = ''
                    self.loadCategories()
                })
            } else {
                alert('Please, fill category name')
            }
        },
        loadAuthors() {
            var self = this
            axios.get('/api/authors/').then(function(response){
                self.authors = response.data
            })
        },
        loadCategories(){
            var self = this
            axios.get('/api/categories/').then(function(response){
                self.categories = response.data
            })
        },
        uploadCover(){
            var self = this
            self.cover_loading = true
            self.cover = self.$refs.cover.files[0]
            let formData = new FormData()
            formData.append('file', this.cover)
            axios.post('/api/covers/',
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }).then(function(response){
                    self.cover_loading = false
                    self.cover_object = response.data
                    self.book_object.cover = response.data.id
                })
        },
        addBook: function() {
            var self = this
            self.is_loading = true
            axios.post('/api/books/', self.book_object)
                .then(function (response) {
                    setTimeout(function(){
                        self.is_loading = false
                        if(response.status === 200 || response.status === 201) {
                            window.location.href = response.data.link
                        }  else {
                            alert('Error. Please, contact admin.')
                        }
                    }, 300);
                }).catch(error => {
                    self.is_loading = false
                    if(error.response.status === 400) {
                        alert('Please, fill all fields. Title, authors, categories and description.')
                    }
                });
        },
        updateBook: function() {
            var self = this
            self.is_loading = true
            axios.put('/api/books/' + self.book_object.id + '/', self.book_object)
                .then(function (response) {
                    setTimeout(function(){
                        self.is_loading = false
                        if(response.status === 200 || response.status === 201) {
                            window.location.href = response.data.link
                        }  else {
                            alert('Error. Please, contact admin.')
                        }
                    }, 300);
                }).catch(error => {
                    self.is_loading = false
                    if(error.response.status === 400) {
                        alert('Please, fill all fields. Title, authors, categories and description.')
                    }
                });
        },
        addUpdateBook() {
            if(this.is_edit) {
                this.updateBook()
            } else {
                this.addBook()
            }
        },
        reset: function () {
            Object.assign(this.$data, getInitialData())
        }
    }
});