require 'json'
require 'rest-client'

input = {'rpn' => "1\n2 3 +"}.to_json

response = RestClient.post "localhost:5000/rpn/solve", input , {content_type: :json, accept: :json}

puts response.code
puts response.body