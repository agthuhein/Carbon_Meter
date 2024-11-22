function validateAddCompanyForm() {
    const companyName = document.getElementById("companyName").value
    const companyemail = document.getElementById("companyEmail").value;
    const sectorType = document.getElementById("sectorType").value;
    const contactPerson = document.getElementById("contactPerson").value
    const address = document.getElementById("address").value
    const postalcode = document.getElementById("postalcode").value

    const companyNameError = document.getElementById(
        "companyName-error"
    );
    const companyEmailError = document.getElementById(
        "companyEmail-error"
    );
    const sectorTypeError = document.getElementById(
        "sectorType-error"
    );
    const contactPersonError = document.getElementById(
        "contactPerson-error"
    );
    const addressError = document.getElementById(
        "address-error"
    );
    const postalCodeError = document.getElementById(
        "postalCode-error"
    );

    companyNameError.textContent = "";
    companyEmailError.textContent = "";
    sectorTypeError.textContent = "";
    contactPersonError.textContent = "";
    addressError.textContent = "";
    postalCodeError.textContent = "";


    let isValid = true;

    if (companyName === "") {
      companyNameError.textContent =
            "Please enter company name.";
        isValid = false;
    }
    if (companyemail === "" || !companyemail.includes("@")) {
      companyEmailError.textContent = "Please enter a valid email address.";
        isValid = false;
    }
    if (sectorType === "") {
      sectorTypeError.textContent =
            "Please select sector.";
        isValid = false;
    }
    if (contactPerson === "") {
      contactPersonError.textContent = "Please enter contact person.";
        isValid = false;
    }
    if (address === "") {
      addressError.textContent = "Please enter contact person.";
        isValid = false;
    }
    if (postalcode === "") {
      postalCodeError.textContent = "Please enter contact person.";
        isValid = false;
    }

    return isValid;
}
