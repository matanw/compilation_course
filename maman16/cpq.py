
import lexer, parser, target_code_producer, errror_logger
if __name__ == '__main__':
  import sys
  file_name=sys.argv[1]
  text = open(file_name).read()
  error_logger=errror_logger.ErrorLogger()
  parser = parser.Parser()#todo: pass error logger to parser
  result = parser.parse(lexer.get_filtered_tokrens(text, error_logger=error_logger))
  print(result) # todo: delete
  target_code_producer.TargetCodeProducer(error_logger=error_logger).go(result)
