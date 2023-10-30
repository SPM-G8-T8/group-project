describe('manage listings page', () => {
    it('view manage listings', () => {
        cy.intercept('http://localhost:8000/staff/?staff_email=john.doe%40example.com', { fixture: 'hr.json' })
        cy.intercept('http://localhost:8000/listing', { fixture: 'listings.json' })
        cy.visit('/')
        cy.visit('/role-listing')
    })

    it('view applicants', () => {
        cy.intercept('http://localhost:8000/staff/?staff_email=john.doe%40example.com', { fixture: 'hr.json' })
        cy.intercept('http://localhost:8000/listing', { fixture: 'listings.json' })
        cy.intercept('http://localhost:8000/listing/1', { fixture: 'listing.json' })
        cy.intercept('http://localhost:8000/applicants/1', { fixture: 'applicant.json' })
        cy.visit('/role-listing/1/1')
    })
})