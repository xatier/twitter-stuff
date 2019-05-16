package main

import (
	"fmt"
	"log"
	"strconv"
	"strings"

	"github.com/dghubble/go-twitter/twitter"
)

func run(api *twitter.Client, startUser string) ([]twitter.User, []twitter.User) {
	log.Println(getRateLimit(api))
	friends := getFriends(api, startUser)

	lessThan500Tweets := find(
		friends.Users,
		func(v twitter.User) bool {
			return v.StatusesCount < 500
		},
		func(v twitter.User) int {
			return v.StatusesCount
		},
	)

	inactiveAccounts := find(
		friends.Users,
		func(v twitter.User) bool {
			if v.Status != nil {
				year, _ := strconv.Atoi(strings.Split(v.Status.CreatedAt, " ")[5])
				return year < 2018
			}
			return true
		},
		func(v twitter.User) int {
			if v.Status != nil {
				year, _ := strconv.Atoi(strings.Split(v.Status.CreatedAt, " ")[5])
				return year
			}
			return 0
		},
	)

	log.Println(getRateLimit(api))
	return lessThan500Tweets, inactiveAccounts
}

func main() {

	log.Println("hello world")
	startUser := "xatierlikelee"
	log.Printf("with @username: %s\n", startUser)
	api := login()
	verify(api)

	lessThan500Tweets, inactiveAccounts := run(api, startUser)

	// TODO(xatier): better report
	fmt.Println("less than 500 tweets")
	for _, v := range lessThan500Tweets {
		fmt.Println(v.ScreenName, v.StatusesCount)
	}

	fmt.Println("inactive users since 2018")
	for _, v := range inactiveAccounts {
		fmt.Println(v.ScreenName, v.StatusesCount)
	}
}
