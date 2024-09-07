### Library System

This is an application to manage library operations

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app library_system
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/library_system
pre-commit install
```
![Screenshot from 2024-09-06 21-21-35](https://github.com/user-attachments/assets/32d5ff61-6639-4882-bea9-1dfb40d8cf01)


There is a child table for the Library Member where his/her books history is kept and the status whether complete or pending, and also the full name field is populated it concatenate the first name and the last name


![Screenshot from 2024-09-06 21-20-25](https://github.com/user-attachments/assets/abf75d14-2e68-4696-a334-f1f79b73b447)

When the book is out of stock, it is not displayed in the list when creating a new issue, only available books are listed. and when a book is returned from the library member it status becomes available, 

![Screenshot from 2024-09-06 21-19-45](https://github.com/user-attachments/assets/1ce5bd71-9068-4fc0-b5b3-9578f0cb82b3)


![Screenshot from 2024-09-06 21-19-02](https://github.com/user-attachments/assets/9424a72c-f117-4b40-a5a4-ebd6b5d5815b)

When a book is issued the Return button is displayed, when it is clicked when the member has not extended then book is returned successfully, but if there is penalty uv to pay first before ur allowed to return the book. The status is pending. Remember the Return date is populated automatically, after 5 days of book issue, which is taken from the Library Settings


![Screenshot from 2024-09-07 08-33-59](https://github.com/user-attachments/assets/282d3544-bdf3-47f1-b3f0-ccb5394d5b69)



When the library member is issued with the book and delays to return the book(Extends) the extended checkbox is marked and the custom button penalize and blacklist appears, when it is clicked, the penalty applies to the library member

![Screenshot from 2024-09-07 08-34-16](https://github.com/user-attachments/assets/77086ac6-e7af-4b96-abd6-34977cd8f394)

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
