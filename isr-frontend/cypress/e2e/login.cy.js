describe('visit home page not logged in', () => {
  it('redirect to login page', () => {
    cy.visit('/')
  })
})


describe('login', () => {
  it('successfully logs in', () => {
    cy.visit('/login')
    Cypress.env('VITE_BASE_URL', 'test')
    cy.get('#input-0').type('john.doe@example.com')
    cy.get('#input-2').type('hr1')
    cy.get('button[type=submit]').click()
    cy.visit("/")
  })
})