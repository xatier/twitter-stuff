package main

import (
	"fmt"
	"runtime"
	"sort"
	"strconv"
	"strings"
	"time"

	"github.com/dghubble/go-twitter/twitter"
	"github.com/dghubble/oauth1"
)

func get_rate_limit(api *twitter.Client) (int, int, time.Time) {
	rateLimits, _, err := api.RateLimits.Status(&twitter.RateLimitParams{
		Resources: []string{"friends"},
	})

	if err != nil {
		_, file, line, _ := runtime.Caller(1)
		fmt.Printf("failed in %s:%d", file, line)
	}

	r := rateLimits.Resources.Friends["/friends/list"]
	return r.Limit, r.Remaining, time.Unix(int64(r.Reset), 0)
}

func getFriends(api *twitter.Client, startUser string) *twitter.Friends {
	// TODO(xatier): make pager work
	friends, _, err := api.Friends.List(&twitter.FriendListParams{
		ScreenName: startUser,
		Count:      200,
	})
	if err != nil {
		panic("can't get friends, QQ")
	}

	return friends
}

func filterUser(xs []twitter.User, pred func(twitter.User) bool) []twitter.User {
	xs1 := make([]twitter.User, 0)
	for _, v := range xs {
		if pred(v) {
			xs1 = append(xs1, v)
		}
	}
	return xs1
}

func find(xs []twitter.User, pred func(twitter.User) bool, key func(twitter.User) int) []twitter.User {
	xs1 := filterUser(xs, pred)
	sort.Slice(xs1, func(i int, j int) bool {
		return key(xs1[i]) < key(xs1[j])
	})
	return xs1
}

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

func login() *twitter.Client {
	// api_keys.go has the following
	// const consumerKey = ""
	// const consumerSecret = ""
	// const accessTokenKey = ""
	// const accessTokenSecret = ""
	config := oauth1.NewConfig(consumerKey, consumerSecret)
	token := oauth1.NewToken(accessTokenKey, accessTokenSecret)
	httpClient := config.Client(oauth1.NoContext, token)
	client := twitter.NewClient(httpClient)

	// client.EnableRateLimiting()
	// client.SetDelay(2*time.Second)

	return client
}

func main() {

	fmt.Println("hello world")
	startUser := "xatierlikelee"
	fmt.Println(startUser)
	api := login()

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
