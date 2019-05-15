package main

import (
	"encoding/json"
	"fmt"
	"log"
	"runtime"
	"sort"
	"time"

	"github.com/dghubble/go-twitter/twitter"
	"github.com/dghubble/oauth1"
)

func get_rate_limit(api *twitter.Client) (int, int, time.Time) {
	rateLimits, _, err := api.RateLimits.Status(&twitter.RateLimitParams{
		Resources: []string{"friends"},
	})

	if err != nil {
		_, file, line, _ := runtime.Caller(0)
		log.Printf("[%s:%d] Failed to get rate limits\n", file, line)
	}

	r := rateLimits.Resources.Friends["/friends/list"]
	return r.Limit, r.Remaining, time.Unix(int64(r.Reset), 0)
}

// only fetch 200 count at a time
func getFriendsPaged(api *twitter.Client, screenName string, cursor int64) *twitter.Friends {
	friends, _, err := api.Friends.List(&twitter.FriendListParams{
		ScreenName: screenName,
		Count:      200,
		Cursor:     cursor,
	})

	if err != nil {
		_, file, line, _ := runtime.Caller(0)
		log.Panicf("[%s:%d] Failed to get friends\n", file, line)
	}

	return friends
}

// fetch all friends
func getFriends(api *twitter.Client, screenName string) *twitter.Friends {
	cursor := int64(-1)
	result := new(twitter.Friends)

	for true {
		pagedFriends := getFriendsPaged(api, screenName, cursor)
		cursor = pagedFriends.NextCursor

		result.Users = append(result.Users, pagedFriends.Users...)

		if cursor == 0 {
			break
		}
	}

	return result
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

// login to Twitter with the given api keys
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

	return client
}

// verify an api handle
func verify(api *twitter.Client) {
	user, _, err := api.Accounts.VerifyCredentials(&twitter.AccountVerifyParams{})
	if err != nil {
		_, file, line, _ := runtime.Caller(0)
		log.Panicf("[%s:%d] Failed to verify API handle\n", file, line)
	}
	prettyPrint(user)
}

// pretty print a struct with as JSON
func prettyPrint(data interface{}) {
	json, err := json.MarshalIndent(data, "", "  ")
	if err != nil {
		_, file, line, _ := runtime.Caller(0)
		log.Printf("[%s:%d] Failed to pretty print\n", file, line)
	}
	fmt.Println(string(json))
}
