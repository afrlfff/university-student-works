USING SYSTEM;
USING SYSTEM.IO;
PUBLIC CLASS COPYFILEUPPER
{
    PUBLIC STATIC VOID MAIN()
    {
        STRING SFROM, STO;
        STREAMREADER SRFROM;
        STREAMWRITER SWTO;

        CONSOLE.WRITE("ENTER INPUT FILE NAME: ");
        SFROM = "C:\\USERS\\DNS\\DESKTOP\\ПРОГА ВУЗ\\2 KURS\\ООП\\LAB7_PART3\\COPYFILEUPPER\\";
        SFROM += CONSOLE.READLINE();
        CONSOLE.WRITE("ENTER OUTPUT FILE NAME: ");
        STO = "C:\\USERS\\DNS\\DESKTOP\\ПРОГА ВУЗ\\2 KURS\\ООП\\LAB7_PART3\\COPYFILEUPPER\\";
        STO += CONSOLE.READLINE();
        TRY
        {
            SRFROM = NEW STREAMREADER(SFROM);
            SWTO = NEW STREAMWRITER(STO);
            STRING SBUFFER;
            WHILE (SRFROM.PEEK() != -1)
            {
                SBUFFER = SRFROM.READLINE().TOUPPER();
                SWTO.WRITELINE(SBUFFER);
            }
            SRFROM.CLOSE();
            SWTO.CLOSE();
        }
        CATCH (FILENOTFOUNDEXCEPTION)
        {
            CONSOLE.WRITELINE("ERROR: FILE WAS NOT FOUND.");
        }
        CATCH (EXCEPTION)
        {
            CONSOLE.WRITELINE("AN ERROR WAS DETECTED.");
        }
    }
}
