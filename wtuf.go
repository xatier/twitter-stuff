package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/dghubble/go-twitter/twitter"
)

func run(api *twitter.Client, startUser string) ([]twitter.User, []twitter.User) {
	fmt.Println(get_rate_limit(api))
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
			} else {
				return true
			}
		},
		func(v twitter.User) int {
			if v.Status != nil {
				year, _ := strconv.Atoi(strings.Split(v.Status.CreatedAt, " ")[5])
				return year
			} else {
				return 0
			}
		},
	)

	fmt.Println(get_rate_limit(api))
	return lessThan500Tweets, inactiveAccounts
}

func main() {

	fmt.Println("hello world")
	startUser := "xatierlikelee"
	fmt.Println(startUser)
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
