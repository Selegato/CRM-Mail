import { Container, Grid2 } from "@mui/material";
import { useForm } from "react-hook-form";
import { useEffect, useState } from "react";

import LoadingButton from "@mui/lab/LoadingButton";
import SendIcon from "@mui/icons-material/Send";
import { yupResolver } from "@hookform/resolvers/yup";

import {
  fetchTenantName,
  fetchReasons,
  fetchRelated,
  submitForm,
} from "../api/Api";
import { ContactSchema } from "./ContactSchema";

import Title from "./Title";
import SuccessAlert from "./SuccessAlert";
import ErrorAlert from "./ErrorAlert";
import CpfInput from "./CpfInput";
import EmailInput from "./EmailInput";
import NomeInput from "./NomeInput";
import LastNameInput from "./LastNameInput";
import PhoneInput from "./PhoneInput";
import CelPhoneInput from "./CelPhoneInput";
import Reason from "./Reason";
import Related from "./Related";
import Mensagem from "./Mensagem";
import DraggerUpload from "./DraggerUpload";

function Form(props) {
  //hooks de states
  const [fileList, setFileList] = useState([]);
  const [reason, setReason] = useState([]);
  const [related, setRelatedTo] = useState([]);
  const [tenantName, setTenantName] = useState("");

  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  //valores padrão do formulário
  const defaultFormValues = {
    documentNumber: "",
    documentType: 1,
    name: "",
    lastName: "",
    email: "",
    phone: "",
    celPhone: "",
    isPrime: false,
    isMobile: false,
    description: "",
    contactReason: "",
    contactRelatedTo: "",
    tenantName: tenantName,
  };

  //hook de form
  const {
    handleSubmit,
    control,
    setValue,
    reset,
    clearErrors,
    formState: { errors },
  } = useForm({
    resolver: yupResolver(ContactSchema),
    defaultValues: defaultFormValues,
  });

  //funcs
  const onSubmit = async (data) => {
    try {
      setIsError(false);
      setIsSuccess(false);
      setIsLoading(true);

      const formData = new FormData();
      //funcao de remover mascaras
      const removeMask = (value) => {
        return value.replace(/[^\d]/g, "");
      };
      //remove mascaras dos campos necessarios
      Object.entries(data).forEach(([key, value]) => {
        if (key === "documentNumber" || key === "celPhone" || key === "phone") {
          value = removeMask(value);
        }
        formData.append(key, value.toString());
      });

      fileList.forEach((file) => {
        formData.append("files", file.originFileObj);
      });

      const responseData = await submitForm(props.tenantId, formData);
      clearErrors();
      reset(defaultFormValues);
      setFileList([]);
      setIsSuccess(true);
      return responseData;
    } catch (error) {
      setIsError(true);
      console.error("Error send the form", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (props.documentNumber) setValue("documentNumber", props.documentNumber);
  }, [props.documentNumber, setValue]);

  useEffect(() => {
    if (props.email) setValue("email", props.email);
  }, [props.email, setValue]);

  useEffect(() => {
    if (props.name) setValue("name", props.name);
  }, [props.name, setValue]);

  useEffect(() => {
    if (props.lastName) setValue("lastName", props.lastName);
  }, [props.lastName, setValue]);

  useEffect(() => {
    if (props.phone) setValue("phone", props.phone);
  }, [props.phone, setValue]);

  useEffect(() => {
    if (props.celPhone) setValue("celPhone", props.celPhone);
  }, [props.celPhone, setValue]);

  useEffect(() => {
    if (props.isPrime) setValue("isPrime", props.isPrime);
  }, [props.isPrime, setValue]);

  useEffect(() => {
    if (props.isMobile) setValue("isMobile", props.isMobile);
  }, [props.isMobile, setValue]);

  //fetch form data from api
  useEffect(() => {
    const fetchDataFromApi = async () => {
      try {
        const [tenantName, reasons, related] = await Promise.all([
          fetchTenantName(props.tenantId),
          fetchReasons(props.tenantId),
          fetchRelated(props.tenantId),
        ]);
        setTenantName(tenantName);
        setReason(reasons);
        setRelatedTo(related);
      } catch (error) {
        console.error("Erro fetch - API", error);
        setIsError(true);
      }
    };
    fetchDataFromApi();
  }, [props.tenantId]);

  return (
    <Container maxWidth="md">
      {/* TITULO */}
      {props.title ? (
        <Title title={props.title} tenantName={tenantName} />
      ) : null}

      <form onSubmit={handleSubmit(onSubmit)}>
        <Grid2 container spacing={2}>
          {/*Alerta Sucesso*/}
          <Grid2 size={{ sm: 12, xs: 12 }}>
            {isSuccess ? <SuccessAlert /> : null}
          </Grid2>

          {/*Alerta Erro*/}
          <Grid2 size={{ sm: 12, xs: 12 }}>
            {isError ? <ErrorAlert /> : null}
          </Grid2>

          {/*Campo CPF*/}
          <Grid2 size={{ sm: 6, xs: 12 }}>
            <CpfInput
              control={control}
              errors={errors}
              documentNumber={props.documentNumber}
            />
          </Grid2>

          {/*Campo E-mail*/}
          <Grid2 size={{ sm: 6, xs: 12 }}>
            <EmailInput control={control} errors={errors} email={props.email} />
          </Grid2>

          {/*Campo Nome*/}
          <Grid2 size={{ sm: 6, xs: 12 }}>
            <NomeInput control={control} errors={errors} name={props.name} />
          </Grid2>

          {/*Campo Sobrenome*/}
          <Grid2 size={{ sm: 6, xs: 12 }}>
            <LastNameInput
              control={control}
              errors={errors}
              lastName={props.lastName}
            />
          </Grid2>

          {/*Campo Telefone*/}
          <Grid2 size={{ sm: 6, xs: 12 }}>
            <PhoneInput control={control} errors={errors} phone={props.phone} />
          </Grid2>

          {/*Campo Celular*/}
          <Grid2 size={{ sm: 6, xs: 12 }}>
            <CelPhoneInput
              control={control}
              errors={errors}
              celPhone={props.celPhone}
            />
          </Grid2>

          {/*Campo Motivo do Contato*/}
          <Grid2 size={{ sm: 6, xs: 12 }}>
            <Reason control={control} errors={errors} reason={reason} />
          </Grid2>

          {/*Campo Relacionado a*/}
          <Grid2 size={{ sm: 6, xs: 12 }}>
            <Related control={control} errors={errors} related={related} />
          </Grid2>

          {/*Campo Mensagem*/}
          <Grid2 size={{ sm: 12, xs: 12 }}>
            <Mensagem control={control} errors={errors} />
          </Grid2>

          {/*Attachments*/}
          <Grid2 size={{ sm: 12, xs: 12 }}>
            <DraggerUpload
              fileList={fileList}
              setFileList={setFileList}
              primaryColor={props.primaryColor}
            />
          </Grid2>

          {/*Botão Enviar*/}
          <Grid2 size={{ sm: 12, xs: 12 }}>
            <LoadingButton
              style={{ backgroundColor: props.primaryColor }}
              endIcon={<SendIcon />}
              loading={isLoading}
              sx={{ mt: 2 }}
              type="submit"
              variant="contained"
              fullWidth={true}
            >
              Send
            </LoadingButton>
          </Grid2>
        </Grid2>
      </form>
    </Container>
  );
}

export default Form;
