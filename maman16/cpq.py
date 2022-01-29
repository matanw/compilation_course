
import lexer, parser, target_code_producer, program_errors, file_manager
if __name__ == '__main__':
  text = file_manager.get_text()
  errors_manager= program_errors.ErrorsManager()
  lexer_result = lexer.get_filtered_tokrens(text, errors_manager)
  files_lines = 1 + text.count('\n')
  parser_result = parser.Parser(errors_manager, files_lines).parse(lexer_result)
  print(parser_result) #todo:delete
  if errors_manager.has_errors():
    errors_manager.log_errors()
    exit() #todo: try  parse evven of errors
  final_code =  target_code_producer.TargetCodeProducer(errors_manager).get_code(parser_result)
  #todo:  add signature
  file_manager.write_output_file(final_code)
