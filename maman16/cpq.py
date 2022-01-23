
import lexer, parser, target_code_producer, errror_logger, file_manager
if __name__ == '__main__':
  text = file_manager.get_text()
  error_logger= errror_logger.ErrorLogger()
  lexer_result = lexer.get_filtered_tokrens(text, error_logger=error_logger)
  parser_result = parser.Parser().parse(lexer_result)
  print(parser_result) #todo:delete
  final_code =  target_code_producer.TargetCodeProducer(error_logger=error_logger).get_code(parser_result)
  #todo:  add signature
  file_manager.write_output_file(final_code)
