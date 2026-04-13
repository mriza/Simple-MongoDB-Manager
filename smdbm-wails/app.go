package main

import (
	"context"
	"encoding/json"
	"fmt"
	"math/rand"
	"os"
	"strings"
	"time"

	"github.com/wailsapp/wails/v2/pkg/runtime"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

// ServerConfig represents a MongoDB server configuration
type ServerConfig struct {
	URL string `json:"url"`
}

// ConfigData holds all server configurations
type ConfigData map[string]ServerConfig

// App struct
type App struct {
	ctx context.Context
}

// NewApp creates a new App application struct
func NewApp() *App {
	return &App{}
}

// startup is called at application startup
func (a *App) startup(ctx context.Context) {
	a.ctx = ctx
	rand.Seed(time.Now().UnixNano())
}

// domReady is called after front-end dom has been loaded
func (a *App) domReady(ctx context.Context) {}

// beforeClose is called when the application is about to quit,
// either by clicking the window close button or calling runtime.Quit.
// Returning true will cause the application to not close.
func (a *App) beforeClose(ctx context.Context) (prevent bool) {
	return false
}

// shutdown is called at application termination
func (a *App) shutdown(ctx context.Context) {}

// LoadServers loads server configurations from smdbm.json
func (a *App) LoadServers() map[string]string {
	configFile := "smdbm.json"
	
	// Try to find the config file in the same directory as the executable
	data, err := os.ReadFile(configFile)
	if err != nil {
		// Try current working directory
		cwd, _ := os.Getwd()
		configFile = cwd + "/smdbm.json"
		data, err = os.ReadFile(configFile)
		if err != nil {
			runtime.LogError(a.ctx, "Config file not found: "+err.Error())
			return map[string]string{}
		}
	}

	var config ConfigData
	err = json.Unmarshal(data, &config)
	if err != nil {
		runtime.LogError(a.ctx, "Failed to parse config: "+err.Error())
		return map[string]string{}
	}

	result := make(map[string]string)
	for name, server := range config {
		result[name] = server.URL
	}

	return result
}

// GenerateRandomPassword generates a random password
func (a *App) GenerateRandomPassword(length int) string {
	characters := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	password := make([]byte, length)
	for i := range password {
		password[i] = characters[rand.Intn(len(characters))]
	}
	return string(password)
}

// CreateDatabaseAndUser creates a database, collection, and user on the selected server
func (a *App) CreateDatabaseAndUser(dbName, username, serverName, role string) string {
	// Get server URL from config
	servers := a.LoadServers()
	serverURL, exists := servers[serverName]
	if !exists {
		return fmt.Sprintf("Error: Server '%s' not found", serverName)
	}

	// Set up MongoDB client with timeout
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	clientOptions := options.Client().ApplyURI(serverURL)
	client, err := mongo.Connect(ctx, clientOptions)
	if err != nil {
		return fmt.Sprintf("Error connecting to MongoDB: %v", err)
	}
	defer client.Disconnect(ctx)

	// Create database and test collection
	db := client.Database(dbName)
	collection := db.Collection("test_collection")
	_, err = collection.InsertOne(ctx, bson.M{"test_field": "test_value"})
	if err != nil {
		return fmt.Sprintf("Error creating database/collection: %v", err)
	}

	// Generate random password
	password := a.GenerateRandomPassword(10)

	// Create user with specified role
	createUserCmd := bson.D{
		{Key: "createUser", Value: username},
		{Key: "pwd", Value: password},
		{Key: "roles", Value: []bson.M{{"role": role, "db": dbName}}},
	}
	err = db.RunCommand(ctx, createUserCmd).Err()
	if err != nil {
		return fmt.Sprintf("Error creating user: %v", err)
	}

	// Extract host from server URL for connection string
	hostPart := serverURL
	if idx := strings.Index(hostPart, "@"); idx != -1 {
		hostPart = hostPart[idx+1:]
	}
	hostPart = strings.TrimRight(hostPart, "/")

	// Remove any trailing slash and database from host part
	if idx := strings.Index(hostPart, "/"); idx != -1 {
		hostPart = hostPart[:idx]
	}

	// Generate connection string for the new user
	connectionURL := fmt.Sprintf("mongodb://%s:%s@%s/%s", username, password, hostPart, dbName)

	return connectionURL
}

// CopyToClipboard copies text to clipboard
func (a *App) CopyToClipboard(text string) {
	runtime.ClipboardSetText(a.ctx, text)
}

// SelectTheme changes the application theme (placeholder for frontend implementation)
func (a *App) SelectTheme(theme string) {
	runtime.LogInfo(a.ctx, "Theme changed to: "+theme)
}
