describe('view all listings page', () => {
  it('view all listings', () => {
    cy.intercept('http://localhost:8000/staff/?staff_email=john.doe%40example.com', { fixture: 'hr.json' })
    cy.intercept('http://localhost:8000/listing/?page=1&hide_expired=true', { fixture: 'listings.json' })
    cy.visit('/', {followRedirect: false})
  })

  it('view one listing', () => {
    cy.intercept('http://localhost:8000/staff/?staff_email=john.doe%40example.com', { fixture: 'hr.json' })
    cy.intercept('http://localhost:8000/listing/?page=1&hide_expired=true', { fixture: 'listings.json' })
    cy.intercept('http://localhost:8000/listing/1', { fixture: 'listing.json' })
    cy.intercept('http://localhost:8000/listing/1/skills', { fixture: 'listing-skills.json' })
    cy.visit('/')
    cy.visit('/role-listing/1', {followRedirect: false})
  })

  it('apply one listing', () => {
    cy.intercept('http://localhost:8000/staff/?staff_email=john.doe%40example.com', { fixture: 'hr.json' })
    cy.intercept('http://localhost:8000/listing/1', { fixture: 'listing.json' })
    cy.intercept('http://localhost:8000/listing/1/skills', { fixture: 'listing-skills.json' })
    cy.intercept('http://localhost:8000/applicants/create/', { fixture: 'apply.json' })
    cy.visit('/role-listing/1', {followRedirect: false})
  })
})