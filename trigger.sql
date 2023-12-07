CREATE TRIGGER Trigger_CodeINSEE
   ON Code_INSEE
   AFTER INSERT
AS 
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    INSERT INTO log_codeINSEE (nom, date) VALUES (SUSER_SNAME(), GETDATE()) 

END