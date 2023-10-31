describe('staff flow', () => {
    Cypress.on('uncaught:exception', (err, runnable) => {
      return false
    })

    it('successfully logs in', () => {
      cy.visit('/login')
      cy.get('#input-0').type('jane.smith@example.com')
      cy.get('#input-2').type('staff1')
      cy.get('button[type=submit]').click()
      cy.url().should('eq', 'http://localhost:3000/')
    }) 

    it('view all listings', () => {
      cy.visit('/')
      cy.get('.v-btn__content').click()
      cy.url().should('eq', 'http://localhost:3000/role-listing/1')
    })

    it('view skills profile', () => {
      cy.visit('/profile')
      cy.get('.v-btn__content').click()
    })
  })
  