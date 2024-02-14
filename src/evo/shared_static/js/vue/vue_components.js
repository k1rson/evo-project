Vue.component('flash-card', {
    props: ['message'],
    delimiters: ['[[', ']]'],
    template: `
                <div class="container mb-3 animate__animated animate__shakeX">
                      <div class="row">
                          <div class="col-12">
                              <div class="card rounded-3 p-2 alert-error-card">
                                  [[ message ]]
                              </div>
                          </div>
                      </div>
                 </div>
    `
})

Vue.component('validate-card', {
    props: ['message'],
    delimiters: ['[[', ']]'],
    template: `
                
    `
})