require 'logger'
require 'json'

require 'rest-client'

Host = "localhost:5000"

# Init logger
$logger = Logger.new(STDOUT)
$logger.level = Logger::DEBUG


def collectResponse(jobId)
  while true do
    response = RestClient.get("#{Host}/rpn/collect/#{jobId}")
    $logger.debug("Collecting response... Return code: #{response.code}")

    case response.code
    when 202
      $logger.debug("Response not ready. Retrying...")
      sleep(0.1)
    when 200
      $logger.debug("Response collected.")
      puts JSON.parse(response.body)['result']['time']
      puts JSON.parse(response.body)['result']['output']
      break
    else
      $logger.error("Undexpected API return code: #{response.code}")
      break
    end
  end
end

def main
  $logger.debug("Reading input for RPN data...")
  input = $stdin.readlines

  $logger.debug("Input ready. Sending RPN job...")
  response = RestClient.post("#{Host}/rpn/solve", {'rpn' => input.join()}.to_json , {content_type: :json, accept: :json})

  case response.code
  when 200
    jobId = JSON.parse(response.body)['job_id']
    $logger.info("Job scheduled. Assigned job id: #{jobId}")
    collectResponse(jobId)
  when 400
    errMessage = response.body
    $logger.error("Bad request: #{errMessage}")
  else
    $logger.error("Undexpected API return code #{response.code}")
  end
end

main()