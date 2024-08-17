package main

import (
	"fmt"
	"sync"
	"time"
)

const conferenceTickets int = 50

var (
	conferenceName   = "Go Conference"
	remainingTickets = uint(conferenceTickets)
	bookings         = make([]UserData, 0)
	wg               = sync.WaitGroup{}
)

type UserData struct {
	firstName       string
	lastName        string
	email           string
	numberOfTickets uint
}

func main() {
	greetUsers()

	for {
		firstName, lastName, email, userTickets := getUserInput()

		if isValid := validateUserInput(firstName, lastName, email, userTickets); isValid {
			bookTicket(userTickets, firstName, lastName, email)
			wg.Add(1)
			go sendTicket(userTickets, firstName, lastName, email)

			firstNames := getFirstNames()
			fmt.Printf("The first names of bookings are: %v\n", firstNames)

			if remainingTickets == 0 {
				fmt.Println("Our conference is booked out. Come back next year.")
				break
			}
		} else {
			fmt.Println("Invalid input. Please try again.")
		}
	}
	wg.Wait()
}

func greetUsers() {
	fmt.Printf("Welcome to %v booking application\n", conferenceName)
	fmt.Printf("We have a total of %v tickets and %v are still available.\n", conferenceTickets, remainingTickets)
	fmt.Println("Get your tickets here to attend")
}

func getFirstNames() []string {
	firstNames := make([]string, len(bookings))
	for i, booking := range bookings {
		firstNames[i] = booking.firstName
	}
	return firstNames
}

func getUserInput() (string, string, string, uint) {
	var (
		firstName   string
		lastName    string
		email       string
		userTickets uint
	)

	fmt.Print("Enter your first name: ")
	fmt.Scan(&firstName)

	fmt.Print("Enter your last name: ")
	fmt.Scan(&lastName)

	fmt.Print("Enter your email address: ")
	fmt.Scan(&email)

	fmt.Print("Enter number of tickets: ")
	fmt.Scan(&userTickets)

	return firstName, lastName, email, userTickets
}

func validateUserInput(firstName, lastName, email string, userTickets uint) bool {
	isValidName := len(firstName) >= 2 && len(lastName) >= 2
	isValidEmail := len(email) >= 5 && contains(email, "@")
	isValidTicketNumber := userTickets > 0 && userTickets <= remainingTickets

	if !isValidName {
		fmt.Println("First name or last name you entered is too short.")
	}
	if !isValidEmail {
		fmt.Println("Email address you entered doesn't contain an @ sign.")
	}
	if !isValidTicketNumber {
		fmt.Println("Number of tickets you entered is invalid.")
	}

	return isValidName && isValidEmail && isValidTicketNumber
}

func contains(s, substr string) bool {
	return len(s) >= len(substr) && s[len(s)-len(substr):] == substr
}

func bookTicket(userTickets uint, firstName, lastName, email string) {
	remainingTickets -= userTickets

	userData := UserData{
		firstName:       firstName,
		lastName:        lastName,
		email:           email,
		numberOfTickets: userTickets,
	}

	bookings = append(bookings, userData)
	fmt.Printf("Thank you %v %v for booking %v tickets. You will receive a confirmation email at %v\n", firstName, lastName, userTickets, email)
	fmt.Printf("%v tickets remaining for %v\n", remainingTickets, conferenceName)
}

func sendTicket(userTickets uint, firstName, lastName, email string) {
	time.Sleep(5 * time.Second)
	ticket := fmt.Sprintf("%v tickets for %v %v", userTickets, firstName, lastName)
	fmt.Println("#################")
	fmt.Printf("Sending ticket:\n %v \nto email address %v\n", ticket, email)
	fmt.Println("#################")
	wg.Done()
}
