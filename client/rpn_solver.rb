require 'json'
require 'rest-client'

input = $stdin.readlines

response = RestClient.post "localhost:5000/rpn/solve", {'rpn' => input.join("")}.to_json , {content_type: :json, accept: :json}

if response.code != 200
    puts "Unexpected error"
else
    jobId = JSON.parse(response.body)['job_id']

    while true do
        response = RestClient.get "localhost:5000/rpn/collect/#{jobId}"

        if response.code == 202
            puts "Response not ready. Retrying..."
            sleep(0.1)
            next
        elsif response.code == 200
            puts JSON.parse(response.body)['result']['time']
            puts JSON.parse(response.body)['result']['output']
            break
        else
            puts "Unexpected error."
        end
    end
end