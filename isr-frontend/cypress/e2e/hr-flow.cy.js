describe('hr flow', () => {
  Cypress.on('uncaught:exception', (err, runnable) => {
    return false
  })

  it('successfully logs in', () => {
    cy.visit('/login')
    cy.get('#input-0').type('john.doe@example.com')
    cy.get('#input-2').type('hr1')
    cy.get('button[type=submit]').click()
    cy.url().should('eq', 'http://localhost:3000/')
  }) 

  it('view one listing', () => {
    cy.visit('/')
    cy.get('.v-btn__content').click()
    cy.url().should('eq', 'http://localhost:3000/role-listing/1')
  })

  it('create a listing', () => {
    cy.visit('/role-listing')
    cy.get('.v-btn--elevated').click()
  })

  it('view applicants', () => {
    cy.intercept('http://localhost:8000/listing/1', { fixture: 'listing.json' })
    cy.intercept('http://localhost:8000/applicants/1', { fixture: 'applicant.json' })
    cy.visit('/role-listing/1/1')   
    cy.url().should('eq', 'http://localhost:3000/role-listing/1/1')
  })
})
