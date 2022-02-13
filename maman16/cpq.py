
import lexer, parser, target_code_producer, program_errors, file_manager
if __name__ == '__main__':
  input_file_path = file_manager.get_and_validate_input_file_path()
  text = file_manager.get_text(input_file_path)
  errors_manager= program_errors.ErrorsManager()
  lexer_result = lexer.get_filtered_tokrens(text, errors_manager)
  files_lines = 1 + text.count('\n')
  parser_result = parser.Parser(errors_manager, files_lines).parse(lexer_result)
  print(parser_result) #todo:delete
  if errors_manager.has_errors():
    errors_manager.log_errors()
    exit() #todo: try  parse evven of errors
  target_code_producer_ =  target_code_producer.TargetCodeProducer(errors_manager)
  target_ops =  target_code_producer_.get_target_ops(parser_result)
  if errors_manager.has_errors():
    errors_manager.log_errors()
    exit()
  final_code = target_code_producer_.get_final_code(target_ops)
  #todo:  add signature
  out_file_path = file_manager.get_out_file_path(input_file_path)
  file_manager.write_output_file(out_file_path,final_code)
