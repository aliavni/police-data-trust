import React, { FormEvent, useState } from "react"
import { EnrollmentCallToAction, EnrollmentHeader, EnrollmentInput } from "../../shared-components"
import { CallToActionTypes, EnrollmentInputNames } from "../../models"
import Layout from "../../shared-components/layout/Layout"

export default function UserLogin() {
  const { EMAIL_ADDRESS, LOGIN_PASSWORD } = EnrollmentInputNames

  const [isSubmitted, setIsSubmitted] = useState(false)

  function handleSubmit($event: FormEvent<HTMLButtonElement>): void {
    $event.preventDefault()
    setIsSubmitted(true)
  }

  return (
    <Layout>
      <section className="enrollmentSection">
        <EnrollmentHeader headerText="Login" />
        <form>
          <EnrollmentInput inputName={EMAIL_ADDRESS} isSubmitted={isSubmitted} />
          <EnrollmentInput inputName={LOGIN_PASSWORD} isSubmitted={isSubmitted} />
          <button className="primaryButton" type="submit" onClick={handleSubmit}>
            Submit
          </button>
        </form>
        <EnrollmentCallToAction callToActionType={CallToActionTypes.REGISTER} />
      </section>
    </Layout>
  )
}